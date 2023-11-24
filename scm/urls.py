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

router = DefaultRouter()

router.register(r'profile', ProfileViewset)

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
    path('profile/', include(router.urls)),
    path('authentication/', include('accounts.urls')),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
