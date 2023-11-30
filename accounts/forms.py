from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField
from django import forms

class CustomSignupForm(SignupForm):
    phone = PhoneNumberField()
    first_name = forms.CharField(max_length=30, label='first_name', required=False)
    last_name = forms.CharField(max_length=30, label='last_name', required=False)
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
# main
