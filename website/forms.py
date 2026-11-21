from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'form-control'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email Address', 'class': 'form-control'}),
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Phone Number', 'class': 'form-control'}),
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password', 'class': 'form-control'}),
    )
    agree_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'You must agree to the Terms & Conditions and Privacy Policy.'},
    )

    def clean_full_name(self):
        return self.cleaned_data['full_name'].strip()

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_phone_number(self):
        return self.cleaned_data['phone_number'].strip()

    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            validate_password(password)
        except ValidationError as error:
            raise forms.ValidationError(error.messages)
        return password
