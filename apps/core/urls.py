from django.urls import path

from .views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('blacklist/', TokenBlacklistView.as_view(), name='token-blacklist'),

    path('obtain/', TokenObtainPairView.as_view(), name='token-obtain'),

    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('verify/', TokenVerifyView.as_view(), name='token-verify'),
]
