"""
Forms for the store app.

Django forms handle user input validation automatically.
Each form maps to an HTML form on a page.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """
    Form for creating a new user account.
    Extends Django's built-in UserCreationForm to add an email field.
    """
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """Save the user with the email field included."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CheckoutForm(forms.Form):
    """
    Form for the checkout page.
    Collects shipping and contact information.
    """
    full_name = forms.CharField(
        max_length=200,
        label='Full Name',
        widget=forms.TextInput(attrs={'placeholder': 'John Doe'})
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'placeholder': 'john@example.com'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label='Phone Number (optional)',
        widget=forms.TextInput(attrs={'placeholder': '+1 234 567 8900'})
    )
    address = forms.CharField(
        label='Street Address',
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': '123 Main Street, Apt 4B'})
    )
    city = forms.CharField(
        max_length=100,
        label='City',
        widget=forms.TextInput(attrs={'placeholder': 'New York'})
    )
    zip_code = forms.CharField(
        max_length=20,
        label='ZIP / Postal Code',
        widget=forms.TextInput(attrs={'placeholder': '10001'})
    )
