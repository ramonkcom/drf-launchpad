from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework_simplejwt.views import (
    TokenObtainPairView as SimpleJwtTokenObtainPairView,
    TokenRefreshView as SimpleJwtTokenRefreshView,
    TokenVerifyView as SimpleJwtTokenVerifyView,
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
class TokenObtainPairView(SimpleJwtTokenObtainPairView):
    """Obtain JWT access and refresh pair from username and password.
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
class TokenRefreshView(SimpleJwtTokenRefreshView):
    """Refresh JWT pair from refresh token.
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
class TokenVerifyView(SimpleJwtTokenVerifyView):
    """Verify whether a JWT token (access or refresh) is valid or not.
    """
