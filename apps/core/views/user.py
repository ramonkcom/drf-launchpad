from rest_framework import (
    generics,
    permissions,
)
from drf_spectacular.utils import extend_schema
from django.urls import reverse
from django.utils.http import urlencode

from ..serializers import UserSerializer


@extend_schema(tags=['User', ])
class UserCreateAPIView(generics.CreateAPIView):
    """Creates a new `User`.
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    def get_serializer_class(self):
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        email = user.emails.first()

        # TODO: Plug the code to send email confirmation here.
        from django.conf import settings
        if settings.DEBUG and not settings.TESTING:
            print(f'{email.address}')

            frontend_params = {'id': email.id,
                               'confirmation_code': email.confirmation_code}
            frontend_url = f'https://FRONTEND_URL/CONFIRM_EMAIL_PATH/?{urlencode(frontend_params)}'
            print(f'{frontend_url=}')

            backend_data = {'confirmation_code': str(email.confirmation_code)}
            backend_url = ('https://BACKEND_URL' +
                           reverse('core:email-confirm', args=[email.pk]))
            print(f'{backend_url=}', f'{backend_data=}')
