"""
Models for the store app.

This file defines the database structure:
- Product: Items available for sale
- Order: A customer's purchase
- OrderItem: A single product line inside an order
"""

from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """
    Represents a product available in the store.
    Each product has a name, price, description, and an optional image.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        """Returns True if the product is available."""
        return self.stock > 0


class Order(models.Model):
    """
    Represents a customer's order.
    An order belongs to a user and contains multiple OrderItems.
    """

    # Order status choices
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    # Shipping / contact information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    @property
    def total_price(self):
        """Calculate the total price of all items in this order."""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Count the total number of items in this order."""
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """
    Represents a single product line inside an order.
    For example: 2x "Wireless Headphones" at $49.99 each.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    # We save the price at time of purchase so it doesn't change if product price changes later
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order.id})"

    @property
    def subtotal(self):
        """Price for this line item: quantity × price."""
        return self.quantity * self.price_at_purchase
