from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from cart.models import Purchase, PurchaseItem


# Create your views here.

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

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
    if not request.user.is_authenticated:
        return redirect('login')

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
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})
    key = str(pk)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
    return redirect('cart')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session['cart']
    if not cart:
        return redirect('cart')
    total = 0
    items_to_save = []
    for product_id in cart:
        print(product_id)
        quantity = cart[product_id]
        product = Product.objects.filter(pk=product_id).first()
        if product:
            subtotal = product.price * quantity
            total += subtotal
            items_to_save.append({'product': product, 'quantity': quantity})

    purchase = Purchase.objects.create(user=request.user, total=total)
    for item in items_to_save:
        PurchaseItem.objects.create(purchase=purchase, product=item['product'], quantity=item['quantity'])

    request.session['cart'] = {}
    return render(request, 'cart/checkout.html')