"""
Cart logic for the store app.

The cart is stored in the user's session (not the database).
A session is temporary storage on the server tied to the user's browser.
This means the cart persists while the browser is open, even if the user
is not logged in.
"""

from decimal import Decimal
from .models import Product


class Cart:
    """
    A simple shopping cart that stores items in the browser session.

    How it works:
    - The cart is a dictionary saved in request.session['cart']
    - Keys are product IDs (as strings)
    - Values are dicts with 'quantity' and 'price'

    Example structure:
    {
        '1': {'quantity': 2, 'price': '29.99'},
        '3': {'quantity': 1, 'price': '49.99'},
    }
    """

    def __init__(self, request):
        """Initialize the cart from the session."""
        self.session = request.session
        # Get existing cart from session, or start a new empty one
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """
        Add a product to the cart, or update its quantity if already in cart.
        """
        product_id = str(product.id)  # Session keys must be strings

        if product_id not in self.cart:
            # New item — add it with the current price
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price),  # Store price as string (JSON safe)
            }
        else:
            # Item already in cart — just update the quantity
            self.cart[product_id]['quantity'] = quantity

        self.save()

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """Mark the session as modified so Django saves it."""
        self.session.modified = True

    def clear(self):
        """Empty the entire cart (called after placing an order)."""
        self.session['cart'] = {}
        self.save()

    def __len__(self):
        """Return the total number of individual items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Loop through cart items, fetching the Product objects from the database.
        Yields a dict for each item with: product, quantity, price, subtotal.
        """
        product_ids = self.cart.keys()
        # Fetch all products in one database query (efficient)
        products = Product.objects.filter(id__in=product_ids)

        # Copy cart so we can add extra data without modifying the session
        cart_copy = dict(self.cart)

        for product in products:
            item = cart_copy[str(product.id)]
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['subtotal'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        """Calculate the total price of all items in the cart."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
