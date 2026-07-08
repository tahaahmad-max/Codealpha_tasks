"""
Admin configuration for the store app.

This registers our models with Django's built-in admin panel,
so the admin can manage products, orders, and order items easily.
"""

from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Configuration for managing products in the admin panel."""
    # Columns shown in the product list
    list_display = ['name', 'price', 'stock', 'created_at']
    # Fields you can filter by (shown on the right sidebar)
    list_filter = ['created_at']
    # Fields you can search by
    search_fields = ['name', 'description']
    # Allow editing price and stock directly from the list view
    list_editable = ['price', 'stock']


class OrderItemInline(admin.TabularInline):
    """
    Shows order items directly inside the Order admin page.
    This is called an 'inline' — it embeds one model inside another.
    """
    model = OrderItem
    extra = 0  # Don't show empty extra rows
    readonly_fields = ['product', 'quantity', 'price_at_purchase']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Configuration for managing orders in the admin panel."""
    list_display = ['id', 'user', 'full_name', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'full_name', 'email']
    # Show order items inside the order detail page
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'created_at']
