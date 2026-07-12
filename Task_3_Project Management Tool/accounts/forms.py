from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    """Registration form with extra fields."""
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': 'form-input'}
    ))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class': 'form-input'}
    ))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Email Address', 'class': 'form-input'}
    ))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-input'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password', 'class': 'form-input'}
        )


class UserUpdateForm(forms.ModelForm):
    """Form to update basic user info."""
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-input'}
    ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'username': forms.TextInput(attrs={'class': 'form-input'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Form to update profile picture and bio."""
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 3,
                                         'placeholder': 'Tell us about yourself...'}),
        }
