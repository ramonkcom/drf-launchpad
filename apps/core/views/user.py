from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
)
from rest_framework import (
    generics,
    permissions,
    response,
    serializers,
    status,
    views,
)

from ..models import User
from ..serializers import UserSerializer


@extend_schema(tags=['Users', ])
class PasswordRecoveryAPIView(views.APIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    @extend_schema(
        request=inline_serializer(
            name='EmailAddressSerializer',
            fields={
                'email': serializers.EmailField(required=True),
            },
        ),
        responses={202: None},
    )
    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email', None)

        if not email:
            error_msg = {'email': _('This field is required.')}
            return response.Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        # NOTE we don't wanna hint whether a user exists or not
        if not user:
            return response.Response(status=status.HTTP_202_ACCEPTED)

        user.generate_reset_token(overwrite=False, save=True)

        recovery_email_msg = user.get_password_recovery_email_message()
        recovery_email_msg.send()

        return response.Response(status=status.HTTP_202_ACCEPTED)


@extend_schema(tags=['Users', ])
class PasswordResetAPIView(views.APIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    @extend_schema(
        request=inline_serializer(
            name='PasswordResetSerializer',
            fields={
                'user_id': serializers.CharField(required=True),
                'reset_token': serializers.CharField(required=True),
                'password_1': serializers.CharField(required=True),
                'password_2': serializers.CharField(required=True),
            },
        ),
        responses={200: UserSerializer},
    )
    def post(self, request, *args, **kwargs):
        data_keys = ['user_id', 'reset_token', 'password_1', 'password_2']
        data = {k: v for k, v in request.data.items() if k in data_keys}

        for key in data_keys:
            value = data.get(key, None)
            if not value:
                error_msg = {key: _('This field is required.')}
                return response.Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        user_id = data.pop('user_id')
        user = User.objects.filter(pk=user_id).first()
        if not user:
            error_msg = {'user_id': _('The user does not exist.'), }
            return response.Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        reset_token = data.pop('reset_token')
        if not user.check_reset_token(reset_token):
            error_msg = {'reset_token': _(
                'The token is invalid or has expired.')}
            return response.Response(error_msg, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(
            user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user.clear_reset_token(save=True)

        return response.Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Users', ])
class UserCreateAPIView(generics.CreateAPIView):
    """Creates a new user.
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    def get_serializer_class(self):
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        email = user.primary_email
        verification_email_msg = email.get_verification_email_message()
        verification_email_msg.send()


@extend_schema(tags=['Users', ])
class UserRetrieveUpdateAPIView(generics.GenericAPIView):
    """Retrieves and updates the authenticated user.
    """

    def get_serializer_class(self):
        return UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            return get_object_or_404(queryset, pk=self.request.user.pk)

        except (TypeError, ValueError, ValidationError):
            raise Http404

    def get(self, request, *args, **kwargs):
        """Retrieves the authenticated user.
        """

        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Updates the authenticated user.
        """

        instance = self.get_object()
        self.check_object_permissions(self.request, instance)

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)
