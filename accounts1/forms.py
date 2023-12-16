from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')

    def custom_signup(self, request, user):
        # Save first_name and last_name to the user model
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
