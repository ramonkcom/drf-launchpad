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
    path('users/me/emails/<str:pk>/confirmation/',
         EmailConfirmationAPIView.as_view(),
         name='email-confirmation'),

    path('users/me/emails/<str:pk>/confirmation/request/',
         EmailConfirmationRequestAPIView.as_view(),
         name='email-confirmation-request'),

    path('users/me/emails/',
         EmailCreateAPIView.as_view(),
         name='email-create'),

    path('users/me/emails/<str:pk>/',
         EmailUpdateDestroyAPIView.as_view(),
         name='email-update-destroy'),

    path('users/password/recovery/',
         PasswordRecoveryAPIView.as_view(),
         name='password-recovery'),

    path('users/password/reset/',
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

    path('users/',
         UserCreateAPIView.as_view(),
         name='user-create'),

    path('users/me/',
         UserRetrieveUpdateAPIView.as_view(),
         name='user-retrieve-update'),
]
