from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended profile for each user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_avatar_url(self):
        """Return avatar URL or a default placeholder."""
        if self.avatar:
            return self.avatar.url
        return None
