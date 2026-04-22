from datetime import timedelta

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from cart.models import Purchase
from store.models import Product, Category

# Create your views here.


def overview(request):
    if admin_check(request) is False:
        return redirect('store:home')

    last_month = timezone.now() - timedelta(days=30)


    return render(request, 'dashboard/overview.html', {
        'purchases_this_month': Purchase.objects.filter(created_at__gte=last_month).count(),
        'user_count': User.objects.count(),
        'product_count': Product.objects.count(),
        'recent_purchases': Purchase.objects.order_by('-created_at')[:5],
        'featured': Product.objects.all().filter(featured=True)[:4]
    })

def products(request):
    if admin_check(request) is False:
        return redirect('store:home')

    product_list = Product.objects.order_by('name')
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'dashboard/products.html', {'products': products_page})


def admin_check(request):
    if not request.user.is_authenticated:
        return redirect('store:login')

    if request.user.userprofile.role not in ('admin', 'moderator') and not request.user.is_superuser:
        return redirect('store:home')

    return True

def product_delete(request, pk):
    if admin_check(request) is False:
        return redirect('store:home')

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    return redirect('dashboard:products')

def product_edit(request, pk):
    if admin_check(request) is False:
        return redirect('store:home')

    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()

    print(request.POST)
    print(product.featured)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.brand = request.POST["brand"]
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.description = request.POST['description']
        product.category = get_object_or_404(Category, pk=request.POST['category'])
        product.featured = 'featured' in request.POST
        product.save()
        if 'delete_image' in request.POST:
            product.image.delete(save=False)
            product.image = None

        if 'image' in request.FILES:
            if 'delete_image' not in request.POST: product.image.delete(save=False)
            product.image = request.FILES['image']
        product.save()
        return redirect('dashboard:products')
    return render(request, 'dashboard/product_edit.html', {
        'product': product,
        'categories': categories
    })
