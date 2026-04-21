from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product

# Create your views here.

def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity'))
    key = str(pk)
    if key in cart:
        cart[key] = cart[key] + quantity
    else:
        cart[key] = quantity
    request.session['cart'] = cart
    return redirect('cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for product_id in cart:
        quantity = cart[product_id]
        product = Product.objects.filter(pk=product_id).first()
        if product:
            subtotal = product.price * quantity
            total += subtotal
            items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, "cart/cart.html", {'items': items, 'total': total})

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    key = str(pk)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
    return redirect('cart')

def checkout(request):
    request.session['cart'] = {}
    return render(request, 'cart/checkout.html')