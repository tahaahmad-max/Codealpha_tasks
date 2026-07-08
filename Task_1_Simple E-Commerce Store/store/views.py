"""
Views for the store app.

Each view function handles one page or one action.
Views receive an HTTP request and return an HTTP response (usually a rendered template).
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm


# ──────────────────────────────────────────────
# PRODUCT VIEWS
# ──────────────────────────────────────────────

def home(request):
    """
    Home page: displays all products in a grid.
    """
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, product_id):
    """
    Product detail page: shows full info for one product.
    get_object_or_404 automatically returns a 404 error page if the product doesn't exist.
    """
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


# ──────────────────────────────────────────────
# CART VIEWS
# ──────────────────────────────────────────────

def cart_view(request):
    """
    Shopping cart page: shows all items currently in the cart.
    """
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def cart_add(request, product_id):
    """
    Adds a product to the cart.
    Called when the user clicks "Add to Cart".
    """
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    # Get the quantity from the form (defaults to 1)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity)

    messages.success(request, f'"{product.name}" added to your cart!')

    # If request came from product detail page, go back there; otherwise go to cart
    next_url = request.POST.get('next', 'cart')
    if next_url == 'detail':
        return redirect('product_detail', product_id=product.id)
    return redirect('cart')


def cart_update(request, product_id):
    """
    Updates the quantity of an item in the cart.
    Called when the user changes the quantity on the cart page.
    """
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product, quantity)
    else:
        cart.remove(product)

    return redirect('cart')


def cart_remove(request, product_id):
    """
    Removes a product completely from the cart.
    """
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.info(request, f'"{product.name}" removed from your cart.')
    return redirect('cart')


# ──────────────────────────────────────────────
# CHECKOUT & ORDER VIEWS
# ──────────────────────────────────────────────

@login_required  # Only logged-in users can checkout
def checkout(request):
    """
    Checkout page: shows the form to enter shipping details.
    On form submit, creates an Order and OrderItems in the database.
    """
    cart = Cart(request)

    # If the cart is empty, redirect back to the home page
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty. Add some products first!')
        return redirect('home')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create the order record
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code'],
            )

            # Create one OrderItem for each product in the cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price_at_purchase=item['price'],
                )

            # Empty the cart now that the order is placed
            cart.clear()

            messages.success(request, 'Your order has been placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
    else:
        # Pre-fill the form with user's email if available
        initial_data = {'email': request.user.email}
        form = CheckoutForm(initial=initial_data)

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
    })


@login_required
def order_confirmation(request, order_id):
    """
    Order confirmation page shown after a successful checkout.
    """
    # Make sure the order belongs to the currently logged-in user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})


@login_required
def order_list(request):
    """
    Shows all past orders for the currently logged-in user.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """
    Shows the details of one specific order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})
