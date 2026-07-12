"""
Context processors for global template data.
"""
from tasks.models import Notification


def unread_notifications(request):
    """Add unread notification count to every template."""
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}
