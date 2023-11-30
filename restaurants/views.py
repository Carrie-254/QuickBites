from .models import Restaurant, MenuItem, Cart, CartItem
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django_daraja.mpesa.core import MpesaClient
import math
from .forms import PaymentForm
from .models import Order, OrderItem, Payment
from django.utils import timezone


def home(request):
    # Fetch popular dishes
    popular_dishes = MenuItem.objects.filter(is_popular=True)[:6]
    
    return render(request, 'home.html', { 'popular_dishes': popular_dishes})

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})


def display_restaurants(request):
    restaurants = Restaurant.objects.all()
    # Calculate star ratings for each restaurant
    for restaurant in restaurants:
        restaurant.full_star_range = range(math.floor(restaurant.rating))
        restaurant.half_star = True if restaurant.rating % 1 != 0 else False
        restaurant.empty_star_range = range(5 - math.ceil(restaurant.rating))
        restaurant.full_star_count = math.floor(restaurant.rating)

    return render(request, 'restaurant_list.html', {'restaurants': restaurants})


def menu_page(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'menu_page.html', {'restaurant': restaurant})


def add_to_cart(request, restaurant_id, menu_item_id):
    get_object_or_404(Restaurant, id=restaurant_id)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)

    if not item_created:
        # Item already in cart, increase quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


def view_cart(request):
    # Get the user's cart
    cart = get_object_or_404(Cart, user=request.user)

    if request.method == 'POST':
        # Handle updates to the cart
        cart_item_id = request.POST.get('cart_item_id')
        new_quantity = int(request.POST.get('new_quantity'))

        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            # If quantity is set to 0, remove the item from the cart
            cart_item.delete()

    # Recalculate total amount
    total_amount = sum(item.menu_item.price * item.quantity for item in cart.cartitem_set.all())

    return render(request, 'view_cart.html', {'cart': cart, 'total_amount': total_amount})


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    # Check if the cart item belongs to the logged-in user
    if cart_item.cart.user != request.user:
        return redirect('view_cart')

    cart_item.delete()
    return redirect('view_cart')


def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    total_amount = sum(item.menu_item.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            # Extract payment details from the form
            phone_number = form.cleaned_data['phone_number']

            # Create an order
            order = Order.objects.create(
                user=user,
                total_amount=total_amount,
                phone_number=phone_number,
            )
            order.created_at = timezone.now()
            order.save()

            # Create order items for each cart item
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    quantity=cart_item.quantity,
                )

            # Create the Payment object
            Payment.objects.create(order=order, amount=total_amount)    

            # Process M-Pesa STK Push
            account_reference = f'order_{order.id}'
            transaction_desc = 'Order Payment'
            callback_url = 'https://api.darajambili.com/express-payment'

            mpesa_client = MpesaClient()

            amount = int(total_amount)

            # Trigger M-Pesa STK Push
            mpesa_client.stk_push(phone_number,amount, account_reference, transaction_desc, callback_url)
            

            # Clear the user's cart after successful order placement
            user.cart.items.clear()

            return HttpResponse("Payment request sent to M-Pesa. Check your phone for STK Push.")
    else:
        form = PaymentForm()

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'form': form,
    }

    return render(request, 'checkout.html', context)


def your_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).prefetch_related('order_items__menu_item')

    context = {
        'orders': orders,
    }

    return render(request, 'your_orders.html', context)


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # deletion logic:
    order.delete()

    messages.success(request, 'Order deleted successfully.')
    return redirect('your_orders')
