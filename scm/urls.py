from django.contrib import admin
from django.urls import path, include  # Add re_path for compatibility
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from accounts.views import Profile, ProfileViewset
from accounts import views
from inventory_management.views import InventoryViewSet
from transaction.views import AbattoirViewSet, BreaderViewSet, BreaderTradeViewSet, AbattoirPaymentViewSet
from accounts.views import get_csrf_token

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
    #   contact=openapi.Contact(email="owillypascal@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),

   public=False,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/csrf_token/', get_csrf_token, name='csrf_token'),
    path('accounts/', include('allauth.account.urls')),  # This includes allauth's registration views
    path('authentication/', include('accounts.urls')),
    path('drf/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
