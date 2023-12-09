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
from transaction.views import AbattoirViewSet, BreaderViewSet, BreaderTradeViewSet, AbattoirPaymentToBreaderViewSet
from inventory_management.views import InventoryBreedViewSet, InventoryBreedSalesViewSet, BreedCutViewSet, BreederTotalSerializer, BreederTotalViewSet
from slaughter_house.views import SlaughterhouseRecordViewSet
# from accounts.views import get_csrf_token
from mpesa_payments.views import MpesaPaymentView

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
    # email_confirm_redirect,
    # password_reset_confirm_redirect,
    GetUserRole,
)

router = DefaultRouter()

router.register(r'profile', ProfileViewset)

# breed sales from transaction
router.register(r'inventory-breed-sales', InventoryBreedSalesViewSet)

router.register(r'inventory-breed-name', InventoryBreedViewSet)

# Ready -breed and trade
router.register(r'breader-trade', BreaderTradeViewSet)
router.register(r'breeder_totals', BreederTotalViewSet, basename='breeder_totals')


# Inventory management

router.register(r'abattoirs', AbattoirViewSet)
router.register(r'breaders', BreaderViewSet)
router.register(r'breed-cut', BreedCutViewSet)
router.register(r'breed-part-count', SlaughterhouseRecordViewSet)
router.register(r'abattoir-payments', AbattoirPaymentToBreaderViewSet)
router.register(r'breader-info-trade', BreaderTradeViewSet, basename='breader-trade')

schema_view = get_schema_view(
   openapi.Info(
      title="SCM APIs",
      default_version='v1',
      description="Test description",
    #   contact=openapi.Contact(email="owillypascal@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),

   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/breader-count/', BreaderCountView.as_view(), name='breader-count'),
    # path('api/total_breeds_supplied/', total_breeds_supplied, name='total_breeds_supplied'),

    path('mpesa-payment/', MpesaPaymentView.as_view(), name = 'mpesa payments'),
    # path('api/csrf_token/', get_csrf_token, name='csrf_token'),
    path('accounts/', include('allauth.account.urls')),  # This includes allauth's registration views
    path('auth/', include('accounts.urls')),
    path('registration/', include('custom_registration.urls')),
    path('drf/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
