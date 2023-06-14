from rest_framework import (
    generics,
    permissions,
    response,
)
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ValidationError

from ..models import User
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


@extend_schema(tags=['User', ])
class UserRetrieveUpdateAPIView(generics.GenericAPIView):
    """Retrieves and updates the authenticated `User`.
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
        """Retrieves the authenticated `User`.
        """

        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Updates the authenticated `User`.
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
