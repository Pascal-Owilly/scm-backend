from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
    VerifyEmailView,
)

from dj_rest_auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
)

from accounts.views import email_confirm_redirect, password_reset_confirm_redirect   
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path, include
from accounts import views

from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static
from accounts.views import ProfileViewset

urlpatterns = [
    #  authentication

    path("register/", RegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path('api/user/role/', views.GetUserRole.as_view(), name='get_user_role'),

    path("register/verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path("register/resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path("account-confirm-email/<str:key>/", email_confirm_redirect, name="account_confirm_email"),
    path("account-confirm-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path("password/reset/confirm/<str:uidb64>/<str:token>/", password_reset_confirm_redirect, name="password_reset_confirm",
    ),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

]