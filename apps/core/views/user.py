from rest_framework import (
    generics,
    permissions,
)
from drf_spectacular.utils import extend_schema

from ..serializers import UserSerializer
from ..utils.auth import send_email_confirmation


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
        send_email_confirmation(user.primary_email)
