# views.py
from allauth.account.views import SignupView
from allauth.account.forms import SignupForm
from allauth.account.utils import complete_signup
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django import forms  # Add this import
from django.http import JsonResponse
from django.middleware.csrf import get_token

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

def register(self, request, **kwargs):
        # Print X-CSRFToken header to terminal
        csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
        print(f'X-CSRFToken: {csrf_token}')

        form = self.get_form()
        if form.is_valid():
            user = self.form_valid(form)
            return self.create_response(request, user)
        else:
            return self.form_invalid(form)


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    id_number = forms.CharField(max_length=20, label='ID Number')
    community = forms.CharField(max_length=100, label='Community')
    market = forms.CharField(max_length=100, label='Market')

class CustomRegistrationView(SignupView):
    form_class = CustomSignupForm

    def create_response(self, request, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({'token': token})

    def register(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = self.form_valid(form)
            return self.create_response(request, user)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user = super().form_valid(form)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.profile.community = form.cleaned_data['community']
        user.profile.id_number = form.cleaned_data['id_number']
        user.profile.market = form.cleaned_data['market']
        user.save()
        return user

    def form_invalid(self, form):
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
