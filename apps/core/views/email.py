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
from django.utils.translation import gettext_lazy as _


from ..models import Email
from ..serializers import EmailSerializer
from ..utils.auth import send_email_confirmation


@extend_schema(tags=['User', ])
class EmailConfirmationAPIView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        return Email.objects.all()

    @extend_schema(
        request=inline_serializer(
            name='ConfirmationCodeSerializer',
            fields={
                'confirmation_code': serializers.CharField(required=True),
            },
        )
    )
    def post(self, request, *args, **kwargs):
        """Confirms an `Email` checking it against its confirmation code.
        """

        confirmation_code = self.request.data.get(
            'confirmation_code', '').strip()

        if not confirmation_code:
            error_msg = _('Confirmation code is required.')
            return response.Response({'confirmation_code': error_msg},
                                     status.HTTP_400_BAD_REQUEST)

        email = self.get_object()

        if not email.check_confirmation_code(confirmation_code):
            error_msg = _('The confirmation code is invalid or has expired.')
            return response.Response({'confirmation_code': error_msg},
                                     status.HTTP_400_BAD_REQUEST)

        email.confirm()
        return response.Response(status=status.HTTP_200_OK)


@extend_schema(tags=['User', ])
class EmailCreateAPIView(generics.CreateAPIView):

    def get_queryset(self):
        return Email.objects.all()

    def get_serializer_class(self):
        return EmailSerializer

    def perform_create(self, serializer):
        email = serializer.save(user=self.request.user)
        send_email_confirmation(email)


@extend_schema(tags=['User', ])
class EmailUpdateDestroyAPIView(generics.GenericAPIView):

    def get_queryset(self):
        return Email.objects.filter(user=self.request.user)

    @extend_schema(
        request=inline_serializer(
            name='EmailSerializer',
            fields={
                'is_primary': serializers.BooleanField(),
            },
        )
    )
    def patch(self, request, *args, **kwargs):
        """Updates the `Email` instance.
        """

        email = self.get_object()
        is_primary = self.request.data.pop('is_primary', False)

        if not is_primary:
            return response.Response(status=status.HTTP_200_OK)

        if not email.is_confirmed:
            error_msg = _(
                'You cannot set an unconfirmed email as primary email.')
            return response.Response({'non_field_errors': error_msg},
                                     status.HTTP_400_BAD_REQUEST)

        user = email.user
        user.email = email.address
        user.save()

        return response.Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Deletes the `Email` instance.
        """

        email = self.get_object()
        if email.is_primary:
            error_msg = _('You cannot delete your primary email.')
            return response.Response({'non_field_errors': error_msg},
                                     status.HTTP_400_BAD_REQUEST)

        email.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
