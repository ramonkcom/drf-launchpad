from django.urls import path

from .views import (
    EmailConfirmationAPIView,
    EmailCreateAPIView,
    EmailUpdateDestroyAPIView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    UserCreateAPIView,
    UserRetrieveUpdateAPIView,
)

app_name = 'core'

urlpatterns = [
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
]
