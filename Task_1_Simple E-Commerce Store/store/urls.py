"""
URL patterns for the store app (products, cart, orders).
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home page — shows all products
    path('', views.home, name='home'),

    # Product detail page
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Shopping cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]
