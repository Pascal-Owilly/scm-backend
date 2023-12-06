# urls.py
from django.urls import path
from .views import CustomRegistrationView, get_csrf_token

urlpatterns = [
    path('register/', CustomRegistrationView.as_view(), name='custom-registration'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),

    # Other URL patterns
]
