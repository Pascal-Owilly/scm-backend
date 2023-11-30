from django.shortcuts import render
from .serializers import ProfileSerializer
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import Profile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError  # Import ValidationError

from django.db import IntegrityError

from allauth.account.views import SignupView
from allauth.account.utils import perform_login
from django.contrib.auth import get_user_model
from accounts.models import Profile

from allauth.account.views import SignupView
from allauth.account.views import SignupView

from allauth.account.views import SignupView as AllAuthSignupView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Profile
from allauth.account.forms import SignupForm
from rest_framework.decorators import action
from allauth.account.views import SignupView as AllAuthSignupView
from phonenumber_field.formfields import PhoneNumberField
from django import forms
from accounts.forms import CustomSignupForm
from django.middleware.csrf import get_token

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
class CustomSignupForm(SignupForm):
    phone = PhoneNumberField()
    username = forms.CharField(max_length=30, label='Username', required=False)
    email = forms.EmailField(max_length=254, label='Email', required=True)

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        # Check if the form has a 'username' field before modifying it
        if 'email' in self.fields:
            self.fields['email'].required = True

    def clean(self):
        cleaned_data = super(CustomSignupForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if not username and not email:
            raise forms.ValidationError('You must provide either a username or an email.')

        return cleaned_data

class RegistrationViewSet(AllAuthSignupView, viewsets.ViewSet):
    serializer_class = ProfileSerializer
    form_class = CustomSignupForm  # Use the custom form

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            user = response.data.get('user', {})
            profile_data = {
                'user_id': user.get('id'),
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'phone_number': request.data.get('phone_number')
            }
            profile = Profile.objects.create(**profile_data)
        return response


#  User role 

class GetUserRole(APIView):
    def get(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get the user's role based on your authentication logic
            user_role = "superuser" if request.user.is_superuser else "regular"
            return Response({"role": user_role})
        else:
            return Response({"role": "anonymous"}, status=status.HTTP_401_UNAUTHORIZED)

# Profile serializers

class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('-created_at')
    serializer_class = ProfileSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            # Get the profile of the authenticated user
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            # Attempt to retrieve the profile to update
            profile = Profile.objects.get(user=request.user)

            # Validate the incoming data with the serializer
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"detail": f"Integrity error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": f"Validation error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )
    
