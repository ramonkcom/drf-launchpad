from django.urls import path

from .views import (
    TokenObtainAPIView,
    TokenRefreshAPIView,
    TokenVerifyAPIView,
    EmailConfirmationAPIView,
    EmailConfirmationRequestAPIView,
    EmailCreateAPIView,
    EmailUpdateDestroyAPIView,
    UserCreateAPIView,
    PasswordRecoveryAPIView,
    PasswordResetAPIView,
    UserRetrieveUpdateAPIView,
)

app_name = 'core'

urlpatterns = [
    path('user/me/email/<str:pk>/confirmation/',
         EmailConfirmationAPIView.as_view(),
         name='email-confirmation'),

    path('user/me/email/<str:pk>/confirmation/request/',
         EmailConfirmationRequestAPIView.as_view(),
         name='email-confirmation-request'),

    path('user/me/email/',
         EmailCreateAPIView.as_view(),
         name='email-create'),

    path('user/me/email/<str:pk>/',
         EmailUpdateDestroyAPIView.as_view(),
         name='email-update-destroy'),

    path('password/recovery/',
         PasswordRecoveryAPIView.as_view(),
         name='password-recovery'),

    path('password/',
         PasswordResetAPIView.as_view(),
         name='password-reset'),

    path('token/',
         TokenObtainAPIView.as_view(),
         name='token'),

    path('token/refresh/',
         TokenRefreshAPIView.as_view(),
         name='token-refresh'),

    path('token/verification/',
         TokenVerifyAPIView.as_view(),
         name='token-verify'),

    path('user/',
         UserCreateAPIView.as_view(),
         name='user-create'),

    path('user/me/',
         UserRetrieveUpdateAPIView.as_view(),
         name='user-retrieve-update'),
]
