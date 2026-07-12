"""
Root URL configuration for the project management tool.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Redirect root to dashboard
    path('', lambda request: redirect('dashboard'), name='home'),

    # Accounts (login, register, logout, profile)
    path('accounts/', include('accounts.urls')),

    # Projects & dashboard
    path('', include('projects.urls')),

    # Tasks, comments, notifications
    path('', include('tasks.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
