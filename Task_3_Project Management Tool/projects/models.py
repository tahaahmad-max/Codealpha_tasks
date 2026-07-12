from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """A project that can contain multiple tasks."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_task_count(self):
        """Return total number of tasks in this project."""
        return self.tasks.count()

    def get_member_count(self):
        """Return total number of members including owner."""
        return self.members.count() + 1  # +1 for owner


class ProjectMember(models.Model):
    """Connects a user to a project as a member."""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only be a member of a project once
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.project.name} ({self.role})"
