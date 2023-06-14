from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


@extend_schema(
    tags=['Authentication'],
)
@extend_schema_view(
    post=extend_schema(
        responses={
            200: inline_serializer(
                name='TokenObtainPairResponse',
                fields={
                    'access': serializers.CharField(),
                    'refresh': serializers.CharField(),
                },
            ),
        },
    ),
)
class AuthenticationAPIView(TokenObtainPairView):
    """Obtain a access and refresh token pair from username and password.
    """


@extend_schema(
    tags=['Authentication'],
)
@extend_schema_view(
    post=extend_schema(
        responses={
            200: inline_serializer(
                name='TokenRefreshResponse',
                fields={
                    'access': serializers.CharField(),
                    'refresh': serializers.CharField(),
                },
            ),
        },
    ),
)
class AuthenticationRenewalAPIView(TokenRefreshView):
    """Obtain a new access and refresh token pair from a refresh token.
    """


@extend_schema(
    tags=['Authentication'],
)
@extend_schema_view(
    post=extend_schema(
        responses={
            200: OpenApiTypes.NONE,
        },
    ),
)
class AuthenticationVerificationAPIView(TokenVerifyView):
    """Verify whether an access or refresh token is valid or not.
    """
