from django import forms
from .models import Task, Comment
from projects.models import ProjectMember
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    """Form to create or edit a task."""

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Task title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Describe the task...'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'priority': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'assigned_to': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, project, *args, **kwargs):
        """Only show users that are members of this project in the assigned_to dropdown."""
        super().__init__(*args, **kwargs)
        # Get all members of this project (including the owner)
        member_ids = ProjectMember.objects.filter(
            project=project
        ).values_list('user_id', flat=True)

        # Include the owner as well
        owner_id = project.owner_id

        # Build the queryset for assignable users
        all_ids = list(member_ids) + [owner_id]
        self.fields['assigned_to'].queryset = User.objects.filter(id__in=all_ids)
        self.fields['assigned_to'].empty_label = '-- Unassigned --'


class CommentForm(forms.ModelForm):
    """Simple form to add a comment."""
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-input comment-input',
                'rows': 2,
                'placeholder': 'Write a comment...'
            })
        }
        labels = {
            'body': ''
        }
