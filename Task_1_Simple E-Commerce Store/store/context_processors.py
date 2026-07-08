"""
Context processors for the store app.

Context processors are functions that add data to every template automatically.
This one adds the cart item count so the navbar can show it on every page.
"""

from .cart import Cart


def cart_count(request):
    """
    Makes 'cart_count' available in every template.
    This is used by the navbar to display the number of items in the cart.
    """
    cart = Cart(request)
    return {'cart_count': len(cart)}
