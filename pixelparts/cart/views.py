from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from cart.models import Purchase, PurchaseItem


# Create your views here.

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('store:login')
    product = get_object_or_404(Product, pk=pk)
    try:
        quantity = int(request.POST.get('quantity'))
    except (ValueError, TypeError):
        return redirect('store:product_detail', pk=pk)
    if quantity < 1 or quantity > product.stock:
        return redirect('store:product_detail', pk=pk)
    cart = request.session.get('cart', {})
    key = str(pk)
    cart[key] = cart.get(key, 0) + quantity
    request.session['cart'] = cart
    return redirect('cart:cart')

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('store:login')

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
        return redirect('store:login')

    cart = request.session.get('cart', {})
    key = str(pk)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
    return redirect('cart:cart')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('store:login')
    if request.method != 'POST':
        return redirect('cart:view_cart')
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart:cart')
    total = 0
    items_to_save = []
    for product_id in cart:
        quantity = cart[product_id]
        product = Product.objects.filter(pk=product_id).first()
        if not product or product.stock < quantity:
            return redirect('cart:view_cart')
        product.stock -= quantity
        try:
            product.save()
        except Exception as e:
            print(f"Error saving product {product.name}: {e}")
            return redirect('cart:view_cart')
        if product:
            subtotal = product.price * quantity
            total += subtotal
            items_to_save.append({'product': product, 'quantity': quantity})

    purchase = Purchase.objects.create(user=request.user, total=total)
    for item in items_to_save:
        PurchaseItem.objects.create(purchase=purchase, product=item['product'], quantity=item['quantity'])

    request.session['cart'] = {}
    return render(request, 'cart/checkout.html')