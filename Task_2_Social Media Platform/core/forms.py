"""
Forms for the Social Media Platform.

Forms handle user input for:
- User Registration
- User Login
- Profile Editing
- Creating/Editing Posts
- Adding Comments
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Post, Comment


class RegisterForm(UserCreationForm):
    """
    Registration form. Extends Django's built-in UserCreationForm
    by adding an email field.
    """
    email      = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    last_name  = forms.CharField(max_length=50, required=False, help_text='Optional.')

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """Save the user and auto-create their profile."""
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name  = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            # Create a blank profile for the new user
            UserProfile.objects.get_or_create(user=user)
        return user


class ProfileEditForm(forms.ModelForm):
    """
    Form to edit a user's profile (bio and profile picture).
    Also allows editing first/last name from the User model.
    """
    first_name = forms.CharField(max_length=50, required=False)
    last_name  = forms.CharField(max_length=50, required=False)

    class Meta:
        model  = UserProfile
        fields = ['bio', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell everyone about yourself...'}),
        }

    def __init__(self, *args, **kwargs):
        """Pre-fill first and last name from the User object."""
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial  = self.instance.user.last_name

    def save(self, commit=True):
        """Save profile and update the related User's name fields."""
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Update first/last name on the User model too
            profile.user.first_name = self.cleaned_data.get('first_name', '')
            profile.user.last_name  = self.cleaned_data.get('last_name', '')
            profile.user.save()
        return profile


class PostForm(forms.ModelForm):
    """
    Form to create or edit a post.
    """
    class Meta:
        model  = Post
        fields = ['caption', 'image']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "What's on your mind?",
            }),
        }


class CommentForm(forms.ModelForm):
    """
    Simple form to add a comment.
    """
    class Meta:
        model  = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Add a comment...'}),
        }
