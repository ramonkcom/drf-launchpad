from django.urls import path

from .views import (
    AuthenticationAPIView,
    AuthenticationRenewalAPIView,
    AuthenticationVerificationAPIView,
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
    path('auth/',
         AuthenticationAPIView.as_view(),
         name='auth'),

    path('auth/renewal/',
         AuthenticationRenewalAPIView.as_view(),
         name='auth-renewal'),

    path('auth/verification/',
         AuthenticationVerificationAPIView.as_view(),
         name='auth-verification'),

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

    path('user/',
         UserCreateAPIView.as_view(),
         name='user-create'),

    path('user/me/',
         UserRetrieveUpdateAPIView.as_view(),
         name='user-retrieve-update'),
]
