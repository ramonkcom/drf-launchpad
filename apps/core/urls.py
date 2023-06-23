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
    UserPasswordRecoveryAPIView,
    UserResetPasswordAPIView,
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

    path('user/',
         UserCreateAPIView.as_view(),
         name='user-create'),

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

    path('user/me/',
         UserRetrieveUpdateAPIView.as_view(),
         name='user-retrieve-update'),

    path('user/<str:pk>/password/',
         UserResetPasswordAPIView.as_view(),
         name='user-password-reset'),

    path('user/password-reset/',
         UserPasswordRecoveryAPIView.as_view(),
         name='user-password-recovery'),
]
