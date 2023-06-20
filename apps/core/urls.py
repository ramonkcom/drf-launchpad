from django.urls import path

from .views import (
    AuthenticationAPIView,
    AuthenticationRenewalAPIView,
    AuthenticationVerificationAPIView,
    EmailConfirmationAPIView,
    EmailCreateAPIView,
    EmailUpdateDestroyAPIView,
    UserCreateAPIView,
    UserPasswordResetAPIView,
    UserPasswordUpdateAPIView,
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

    path('user/email/<str:pk>/confirmation/',
         EmailConfirmationAPIView.as_view(),
         name='email-confirmation'),

    path('user/email/',
         EmailCreateAPIView.as_view(),
         name='email-create'),

    path('user/email/<str:pk>/',
         EmailUpdateDestroyAPIView.as_view(),
         name='email-update-destroy'),

    path('user/me/',
         UserRetrieveUpdateAPIView.as_view(),
         name='user-retrieve-update'),

    path('user/<str:pk>/password/',
         UserPasswordUpdateAPIView.as_view(),
         name='user-password-update'),

    path('user/password-reset/',
         UserPasswordResetAPIView.as_view(),
         name='user-password-reset'),
]
