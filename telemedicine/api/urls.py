from django.urls import path, include
from dj_rest_auth.registration.views import ConfirmEmailView, VerifyEmailView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Users: Preview
    path('accounts/', include('accounts.urls')),

    # Login
    path('auth/', include('dj_rest_auth.urls')),

    # Register
    path('auth/register/', include('dj_rest_auth.registration.urls'), name='rest_register'),

    # Email Confirmation
    path('account-confirm-email/<key>/',
         ConfirmEmailView.as_view(template_name='account/email_verification.html'),
         name='account_confirm_email'),
    path('account-confirm-email/',
         VerifyEmailView.as_view(),
         name='account_email_verification_sent'),

    # Password Reset
    path('auth/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
]
