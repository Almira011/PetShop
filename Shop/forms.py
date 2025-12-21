from django import forms
from django.contrib.auth.models import User
from .models import Customer


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email', 'address']
        labels = {
            'name': 'Full Name',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'address': 'Shipping Address',
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
