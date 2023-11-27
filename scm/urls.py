from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import UserDetailsView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from transaction.views import AbattoirViewSet, BreaderViewSet, BreaderTradeViewSet, AbattoirPaymentViewSet
from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    PasswordResetView,
    LoginView,
    UserDetailsView,
    LogoutView,
)
from allauth.account.views import (
    LoginView as AllAuthLoginView,
    LogoutView as AllAuthLogoutView,
    PasswordResetDoneView as AllAuthPasswordResetDoneView,
)

from accounts.views import (
    Profile,
    ProfileViewset,
    email_confirm_redirect,
    password_reset_confirm_redirect,
    GetUserRole,
)
from inventory_management.views import InventoryViewSet
from accounts.views import get_csrf_token

# Create a single router for 'profile', 'inventory', and other views
router = DefaultRouter()
router.register(r'profile', ProfileViewset)
router.register(r'inventory', InventoryViewSet)

# transaction

router.register(r'abattoirs', AbattoirViewSet)
router.register(r'breaders', BreaderViewSet)
router.register(r'breader-trade', BreaderTradeViewSet)
router.register(r'abattoir-payments', AbattoirPaymentViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="SCM APIs",
        default_version='v1',
        description="Test description",
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include all views under the 'admin' URL

    # csrf token
    path('csrf_token/', get_csrf_token, name='csrf_token'),

    # Include allauth authentication views
    path('accounts/', include('allauth.account.urls')),  # This includes allauth's registration views
    path('api/user/details/', UserDetailsView.as_view(), name='user-details'),
    path('api/user/role/', GetUserRole.as_view(), name='get_user_role'),

    path('swagger/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)