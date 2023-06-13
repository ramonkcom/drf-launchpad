from django.urls import path

from .views import (
    EmailConfirmationAPIView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    UserCreateAPIView,
)

app_name = 'core'

urlpatterns = [
    path('email/<str:pk>/confirmation/',
         EmailConfirmationAPIView.as_view(),
         name='email-confirm'),

    path('token/obtain/',
         TokenObtainPairView.as_view(),
         name='token-obtain'),

    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token-refresh'),

    path('token/verify/',
         TokenVerifyView.as_view(),
         name='token-verify'),

    path('user/',
         UserCreateAPIView.as_view(),
         name='user-create'),
]
