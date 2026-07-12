from django.contrib import admin
from .models import Task, Comment, Notification


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'priority', 'assigned_to', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'project__name', 'assigned_to__username']
    list_editable = ['status', 'priority']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'task', 'created_at', 'body_preview']
    list_filter = ['created_at']
    search_fields = ['author__username', 'task__title', 'body']

    def body_preview(self, obj):
        return obj.body[:60] + '...' if len(obj.body) > 60 else obj.body
    body_preview.short_description = 'Comment Preview'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['recipient__username', 'message']
    list_editable = ['is_read']
