from django.urls import path

from .views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('obtain/', TokenObtainPairView.as_view(), name='token-obtain'),

    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('verify/', TokenVerifyView.as_view(), name='token-verify'),
]
