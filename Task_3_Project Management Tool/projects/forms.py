from django import forms
from .models import Project, ProjectMember
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    """Form to create or edit a project."""
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Project name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Describe this project...'
            }),
        }


class AddMemberForm(forms.Form):
    """Form to add a member to a project by username."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter username to add...'
        })
    )
    role = forms.ChoiceField(
        choices=ProjectMember.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    def clean_username(self):
        """Validate that the user exists."""
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f'No user found with username "{username}".')
        return username
