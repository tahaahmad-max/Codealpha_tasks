"""
Admin panel configuration.
Registers all models so the admin can manage them from /admin/.
"""

from django.contrib import admin
from .models import UserProfile, Post, Comment, Like, Follow


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'bio']
    search_fields = ['user__username', 'bio']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ['author', 'caption', 'created_at']
    list_filter   = ['created_at']
    search_fields = ['author__username', 'caption']
    ordering      = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ['author', 'post', 'text', 'created_at']
    search_fields = ['author__username', 'text']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display  = ['user', 'post']
    search_fields = ['user__username']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display  = ['follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']
