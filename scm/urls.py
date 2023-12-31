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
from logistics.views import LogisticsStatusViewSet, OrderViewSet, ShipmentProgressViewSet, ArrivedOrderViewSet


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

from transaction.views import AbattoirPaymentToBreaderViewSet

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
    RoleListView,
    PaymentViewSet, CustomerServiceViewSet
)

# Payments
from payments.views import make_payment

router = DefaultRouter()
app_name = 'payments'

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

# 
router.register(r'abattoir-payments-to-breeder', AbattoirPaymentToBreaderViewSet, basename='abattoir-payments-to-breeder')

router.register(r'abattoir-payments-to-breeders/search-payment-by-code', AbattoirPaymentToBreaderViewSet, basename='search-payment-by-code')

# custom registration

router.register(r'login', CustomUserLoginViewSet, basename='login')
router.register(r'register', CustomUserRegistrationViewSet, basename='register')
router.register(r'logout', CustomLogoutViewSet, basename='logout')
router.register(r'profiles', UserProfileViewSet, basename='profile')

# Payments

# router.register(r'payments-to-breeder', PaymentViewSet, basename='payment_to_breeder')
router.register(r'payments-to-breeder', AbattoirPaymentToBreaderViewSet, basename='payment_to_breeder')

# Customer service
router.register(r'customer-service', CustomerServiceViewSet, basename='customer-service')

# Logistics management
router.register(r'logistics-status', LogisticsStatusViewSet, basename='logistics')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'shipment-progress', ShipmentProgressViewSet, basename='shipment-progress')
router.register(r'arrived-order', ArrivedOrderViewSet, basename='arrived-order')




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
    # path('make_payment/<int:breeder_trade_id>/', make_payment, name='make_payment'),
    path('api/make-payment/<int:breeder_trade_id>/', make_payment, name='make_epayment'),
   # paymens list
    path('api/payments-list/', PaymentViewSet.as_view({'get': 'list_payments'}), name='list_payments'),
  
    # Search breeder by code 
    path('api/abattoir-payments-to-breeder/search-payment-by-code/', AbattoirPaymentToBreaderViewSet.as_view({'get': 'search_payment_by_code'}), name='search-payment-by-code'),
    
    # customer service viewset

    path('mpesa-payment/', MpesaPaymentView.as_view(), name = 'mpesa payments'),
    # path('api/csrf_token/', get_csrf_token, name='csrf_token'),
    # path('accounts/', include('allauth.account.urls')),  # This includes allauth's registration views
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
