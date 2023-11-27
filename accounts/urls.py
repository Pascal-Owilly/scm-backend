# from django.urls import path, include
# from dj_rest_auth.registration.views import (
#     ResendEmailVerificationView,
#     VerifyEmailView,
# )
# from dj_rest_auth.views import (
#     PasswordResetConfirmView,
#     PasswordResetView,
#     LogoutView,
# )
# from accounts.views import email_confirm_redirect, password_reset_confirm_redirect   
# from dj_rest_auth.registration.views import RegisterView
# from dj_rest_auth.views import LoginView, UserDetailsView
# from allauth.account.views import LoginView as AllAuthLoginView, LogoutView as AllAuthLogoutView

# from django.conf import settings
# from django.conf.urls.static import static
# from accounts.views import ProfileViewset
# from accounts import views

# urlpatterns = [
#     # Authentication
#     path("register/", RegisterView.as_view(), name="rest_register"),
#     path("login/", LoginView.as_view(), name="rest_login"),
#     path("logout/", LogoutView.as_view(), name="rest_logout"),
#     path("user/", UserDetailsView.as_view(), name="rest_user_details"),
#     path('api/user/role/', views.GetUserRole.as_view(), name='get_user_role'),

#     # Allauth URLs
#     path('accounts/login/', AllAuthLoginView.as_view(), name='account_login'),
#     path('accounts/logout/', AllAuthLogoutView.as_view(), name='account_logout'),
#     path('accounts/verify-email/', VerifyEmailView.as_view(), name='account_verify_email'),
#     path('accounts/resend-email/', ResendEmailVerificationView.as_view(), name='account_resend_email'),
#     path('accounts/password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
#     path('accounts/password/reset/confirm/<str:uidb64>/<str:token>/', password_reset_confirm_redirect, name='account_reset_password_confirm'),
# ]

