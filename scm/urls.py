from django.contrib import admin
from django.urls import path, include  # Add re_path for compatibility
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
# from accounts.views import Profile, ProfileViewset
# from accounts import views
from transaction.views import AbattoirViewSet, BreaderViewSet, BreaderTradeViewSet, AbattoirPaymentToBreaderViewSet, BreaderCountView
from inventory_management.views import InventoryBreedViewSet, InventoryBreedSalesViewSet, BreedCutViewSet, BreederTotalSerializer, BreederTotalViewSet, BreedCutTotalViewSet
from slaughter_house.views import SlaughterhouseRecordViewSet
# from accounts.views import get_csrf_token
from mpesa_payments.views import MpesaPaymentView
from invoice_generator.views import InvoiceViewSet, BuyerViewSet
from slaughter_house.views import supply_vs_demand_statistics

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

# from accounts.views import (
#     Profile,
#     ProfileViewset,
#     # email_confirm_redirect,
#     # password_reset_confirm_redirect,
#     GetUserRole,
# )

from custom_registration.views import (
    CustomTokenObtainPairView,
    CustomUserLoginViewSet,
    CustomUserRegistrationViewSet,
    CustomLogoutViewSet,
    CustomTokenRefreshView,
    UserProfileView,
    UserProfileViewSet,
    GetUserRole,
    UserProfilesListView,
    RoleListView

)

# Payments
from payments.views import request_payment, make_equity_bank_payment

router = DefaultRouter()

# router.register(r'profile', ProfileViewset)

# breed sales from transaction
router.register(r'inventory-breed-sales', InventoryBreedSalesViewSet)

router.register(r'inventory-breed-name', InventoryBreedViewSet)

# Ready -breed and trade
router.register(r'breader-trade', BreaderTradeViewSet)
router.register(r'breeder_totals', BreederTotalViewSet, basename='cut_totals')
router.register(r'part_totals_count', BreedCutTotalViewSet, basename='breeder_totals')

# Inventory management

router.register(r'abattoirs', AbattoirViewSet)
router.register(r'breaders', BreaderViewSet)
router.register(r'breed-cut', BreedCutViewSet)
router.register(r'slaughtered-list', SlaughterhouseRecordViewSet)
router.register(r'abattoir-payments', AbattoirPaymentToBreaderViewSet)
router.register(r'breader-info-trade', BreaderTradeViewSet, basename='breader-trade')

# custom registration

router.register(r'login', CustomUserLoginViewSet, basename='login')
router.register(r'register', CustomUserRegistrationViewSet, basename='register')
router.register(r'logout', CustomLogoutViewSet, basename='logout')
router.register(r'profiles', UserProfileViewSet, basename='profile')


# Invoice

# Create a router and register our viewsets with it.
router.register(r'generate-invoice', InvoiceViewSet)
router.register(r'buyers', BuyerViewSet)

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

    # custom registration

    path('auth/token/', CustomTokenObtainPairView.as_view(), name='auth-token'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/', UserProfileView.as_view(), name='user-profile'),  # Use .as_view() for class-based views
    path('get-user-role/', GetUserRole.as_view(), name='get_user_role'),
    path('auth/all-profiles/', UserProfilesListView.as_view(), name='get_user_role'),
    path('api/roles/', RoleListView.as_view(), name='role-list'),


    path('api/', include(router.urls)),
    path('api/breader-count/', BreaderCountView.as_view(), name='breader-count'),
    # path('api/total_breeds_supplied/', total_breeds_supplied, name='total_breeds_supplied'),
    
    path('api/supply-vs-demand/', supply_vs_demand_statistics, name='supply_vs_demand_statistics'),

    # Equity bank Payments
    path('api/request-payment-equity/<int:breader_trade_id>/', request_payment, name='request_payment'),
    path('api/make_equity_bank_payment/', make_equity_bank_payment, name='make_equity_bank_payment'),



    path('mpesa-payment/', MpesaPaymentView.as_view(), name = 'mpesa payments'),
    # path('api/csrf_token/', get_csrf_token, name='csrf_token'),
    path('accounts/', include('allauth.account.urls')),  # This includes allauth's registration views
    # path('auth/', include('accounts.urls')),
    # path('registration/', include('custom_registration.urls')),
    path('drf/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
