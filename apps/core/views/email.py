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


@extend_schema(tags=['User', ])
class EmailConfirmationAPIView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        return Email.objects.filter(confirmation_date=None)

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
