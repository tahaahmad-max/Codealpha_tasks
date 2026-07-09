"""
Database models for the Social Media Platform.

Models:
- UserProfile  : Extra info for each user (bio, picture)
- Post         : A text/image post made by a user
- Comment      : A comment on a post
- Like         : A like on a post
- Follow       : A follow relationship between two users
"""

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends Django's built-in User with extra fields.
    One profile per user (OneToOne relationship).
    """
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio        = models.TextField(blank=True, max_length=300)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_followers_count(self):
        """Return how many users follow this profile's user."""
        return Follow.objects.filter(following=self.user).count()

    def get_following_count(self):
        """Return how many users this profile's user follows."""
        return Follow.objects.filter(follower=self.user).count()

    def get_posts_count(self):
        """Return total number of posts by this user."""
        return Post.objects.filter(author=self.user).count()


class Post(models.Model):
    """
    A post created by a user. Can have a caption and an optional image.
    """
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption    = models.TextField(max_length=2000)
    image      = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest posts first

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at:%Y-%m-%d %H:%M}"

    def get_likes_count(self):
        """Return total likes on this post."""
        return Like.objects.filter(post=self).count()

    def get_comments_count(self):
        """Return total comments on this post."""
        return Comment.objects.filter(post=self).count()

    def is_liked_by(self, user):
        """Check if a specific user has liked this post."""
        return Like.objects.filter(post=self, user=user).exists()


class Comment(models.Model):
    """
    A comment left by a user on a post.
    """
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text       = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Oldest comments first

    def __str__(self):
        return f"Comment by {self.author.username} on Post #{self.post.id}"


class Like(models.Model):
    """
    Represents a user liking a post.
    A user can only like a post once (unique_together enforces this).
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} liked Post #{self.post.id}"


class Follow(models.Model):
    """
    Represents a follow relationship.
    'follower' follows 'following'.
    """
    follower  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Can't follow someone twice

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
