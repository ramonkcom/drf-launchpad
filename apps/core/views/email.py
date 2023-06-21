from django.http import Http404
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

from ..models import Email
from ..serializers import EmailSerializer


@extend_schema(tags=['User', ])
class EmailConfirmationAPIView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        return Email.objects.all()

    def get_serializer_class(self):
        return EmailSerializer

    @extend_schema(
        request=inline_serializer(
            name='ConfirmationCodeInlineSerializer',
            fields={
                'confirmation_code': serializers.CharField(required=True),
            },
        ),
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
        data = self.get_serializer(email).data

        return response.Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=['User', ])
class EmailConfirmationRequestAPIView(generics.GenericAPIView):

    # NOTE This view does not use DjangoObjectPermissions because
    # django-guardian understands POST requests as an attempt to create a new
    # object, and thus it checks for the `add_email` permission, which is not
    # what we want. Security in this aspect is being handled by the queryset.
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        if not self.request.user or self.request.user.is_anonymous:
            return Email.objects.none()

        return Email.objects.filter(user=self.request.user)

    @extend_schema(
        request=None,
        responses={202: None},
    )
    def post(self, request, *args, **kwargs):
        """Requests a new confirmation link for an `Email`.
        """

        email = self.get_object()

        if email.is_confirmed:
            error_msg = _('The email is already confirmed.')
            return response.Response({'non_field_errors': error_msg},
                                     status.HTTP_400_BAD_REQUEST)

        email.regenerate_confirmation_code(save=True)
        verification_email = email.get_verification_email()
        verification_email.send()

        return response.Response(status=status.HTTP_202_ACCEPTED)


@extend_schema(tags=['User', ])
class EmailCreateAPIView(generics.CreateAPIView):
    """Adds a new `Email` to the authenticated user.
    """

    def get_queryset(self):
        if not self.request.user:
            return Email.objects.none()

        return Email.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return EmailSerializer

    def perform_create(self, serializer):
        email = serializer.save(user=self.request.user)
        verification_email = email.get_verification_email()
        verification_email.send()


@extend_schema(tags=['User', ])
class EmailUpdateDestroyAPIView(generics.GenericAPIView):

    def get_queryset(self):
        if not self.request.user:
            return Email.objects.none()

        return Email.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return EmailSerializer

    @extend_schema(
        request=inline_serializer(
            name='EmailUpdateInlineSerializer',
            fields={
                'is_primary': serializers.BooleanField(required=True),
            },
        ),
    )
    def patch(self, request, *args, **kwargs):
        """Updates an `Email` of the authenticated user.
        """

        email = self.get_object()
        is_primary = self.request.data.pop('is_primary', None)

        if is_primary is None:
            error_msg = _('is_primary is required.')
            return response.Response({'is_primary': error_msg},
                                     status.HTTP_400_BAD_REQUEST)

        if not is_primary:
            error_msg = _('You cannot directly make an email not primary. '
                          'Set another email as primary instead.')
            return response.Response({'non_field_errors': error_msg},
                                     status.HTTP_400_BAD_REQUEST)

        if not email.is_confirmed:
            error_msg = _(
                'You cannot set an unconfirmed email as primary email.')
            return response.Response({'non_field_errors': error_msg},
                                     status.HTTP_400_BAD_REQUEST)

        user = email.user
        user.email = email.address
        user.save()

        data = self.get_serializer(email).data

        return response.Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Deletes an `Email` from the authenticated user.
        """

        email = self.get_object()
        if email.is_primary:
            error_msg = _('You cannot delete your primary email.')
            return response.Response({'non_field_errors': error_msg},
                                     status.HTTP_400_BAD_REQUEST)

        email.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
