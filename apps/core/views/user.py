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
)

from ..models import User
from ..serializers import UserSerializer


@extend_schema(tags=['User', ])
class UserCreateAPIView(generics.CreateAPIView):
    """Creates a new user.
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    def get_serializer_class(self):
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        verification_email = user.primary_email.get_verification_email()
        verification_email.send()


@extend_schema(tags=['User', ])
class UserPasswordRecoveryAPIView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    def get_serializer_class(self):
        return UserSerializer

    def get_queryset(self):
        if email := self.request.data.get('email', None):
            return User.objects.filter(email=email)

        return User.objects.none()

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

        user = self.get_queryset().first()

        if not user:
            return response.Response(status=status.HTTP_202_ACCEPTED)

        user.generate_reset_token(overwrite=False, save=True)

        reset_email = user.get_password_reset_email()
        reset_email.send()

        return response.Response(status=status.HTTP_202_ACCEPTED)


@extend_schema(tags=['User', ])
class UserResetPasswordAPIView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    def get_serializer_class(self):
        return UserSerializer

    def get_queryset(self):
        user_id = self.request.data.get('user_id', None)

        if user_id:
            return User.objects.filter(pk=user_id)

        return User.objects.none()

    @extend_schema(
        request=inline_serializer(
            name='ResetPasswordSerializer',
            fields={
                'reset_token': serializers.CharField(required=True),
                'password_1': serializers.CharField(required=True),
                'password_2': serializers.CharField(required=True),
            },
        ),
    )
    def patch(self, request, *args, **kwargs):
        user_id = self.request.data.get('user_id', None)
        reset_token = self.request.data.get('reset_token', None)
        password_1 = self.request.data.get('password_1', None)
        password_2 = self.request.data.get('password_2', None)

        if not user_id:
            error_msg = {'user_id': _('This field is required.'), }
            return response.Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        if not reset_token:
            error_msg = {'reset_token': _('This field is required.'), }
            return response.Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        if not password_1 and not password_2:
            error_msg = {'password_1': _('This field is required.'),
                         'password_2': _('This field is required.'), }
            return response.Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_queryset().first()
        if not user:
            raise Http404

        if not user.check_reset_token(reset_token):
            error_msg = {'reset_token': _(
                'Request is invalid or has expired.')}
            return response.Response(error_msg, status=status.HTTP_403_FORBIDDEN)

        data = {
            'password_1': password_1,
            'password_2': password_2,
        }
        serializer = self.get_serializer(
            user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user.clear_reset_token(save=True)

        return response.Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['User', ])
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
            raise Http404  # pylint: disable=raise-missing-from

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
