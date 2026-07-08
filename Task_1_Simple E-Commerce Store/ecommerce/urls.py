"""
Main URL configuration for the ecommerce project.
All URL routes are defined or included here.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # All store-related pages (products, cart, orders, etc.)
    path('', include('store.urls')),

    # Authentication pages (login, register, logout)
    path('auth/', include('store.auth_urls')),
]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
