from datetime import timedelta

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from cart.models import Purchase
from store.models import Product, Category

# Create your views here.


def overview(request):
    res = admin_check(request)
    if res:
        return res

    last_month = timezone.now() - timedelta(days=30)

    return render(request, 'dashboard/overview.html', {
        'purchases_this_month': Purchase.objects.filter(created_at__gte=last_month).count(),
        'user_count': User.objects.count(),
        'product_count': Product.objects.count(),
        'recent_purchases': Purchase.objects.order_by('-created_at')[:5],
        'featured': Product.objects.all().filter(featured=True)[:4]
    })

def products(request):
    res = admin_check(request)
    if res:
        return res

    product_list = Product.objects.order_by('name')
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'dashboard/products.html', {'products': products_page})


def admin_check(request):

    if not request.user.is_authenticated:
        return redirect('store:login')

    try:
        if not request.user.is_superuser and request.user.userprofile.role not in ('admin', 'moderator'):
            return redirect('store:home')
    except:
        return redirect('store:home')

    return None

def product_delete(request, pk):
    res = admin_check(request)
    if res:
        return res

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    return redirect('dashboard:products')

def product_edit(request, pk):
    res = admin_check(request)
    if res:
        return res

    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        try:
            name = request.POST.get('name','').strip()[:50]
            brand = request.POST.get('brand','').strip()[:50]
            price = float(request.POST.get('price',0))
            stock = int(request.POST.get('stock',0))
            category_id = request.POST.get('category')

            if not name or not brand or price < 0 or stock < 0 or not category_id:
                return render(request, 'dashboard/product_edit.html', {
                    'product': product,
                    'categories': categories,
                    'error': 'Invalid input'
                })


            product.name = name
            product.brand = brand
            product.price = price
            product.stock = stock
            product.description = request.POST.get('description','').strip()[:2000]
            product.category = get_object_or_404(Category, pk=category_id)
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
        except (ValueError, TypeError):
            return render(request, 'dashboard/product_edit.html', {
                'product': product,
                'categories': categories,
                'error': 'Invalid input'
            })
    return render(request, 'dashboard/product_edit.html', {
        'product': product,
        'categories': categories
    })

def categories(request):
    res = admin_check(request)
    if res:
        return res

    category_list = Category.objects.order_by('name')
    paginator = Paginator(category_list, 10)
    page = request.GET.get('page')
    categories_page = paginator.get_page(page)
    return render(request, 'dashboard/categories.html', {'categories': categories_page})

def category_delete(request, pk):
    res = admin_check(request)
    if res:
        return res

    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
    return redirect('dashboard:categories')

def category_edit(request, pk):
    res = admin_check(request)
    if res:
        return res

    category = get_object_or_404(Category, pk=pk)
    all_categories = Category.objects.exclude(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name','').strip()[:50]
        icon = request.POST.get('bootstrap_icon_code','').strip()[:50]

        if not name:
            return render(request, 'dashboard/category_edit.html', {
                'category': category,
                'all_categories': all_categories,
                'error': 'Name is required'
            })
        category.name = name
        category.bootstrap_icon_code = icon
        parent_id = request.POST.get('parent')
        if parent_id:
            try:
                parent = get_object_or_404(Category, pk=parent_id)
                if parent.pk == category.pk:
                    return render(request, 'dashboard/category_edit.html', {
                        'category': category,
                        'all_categories': all_categories,
                        'error': 'A category cannot be a parent of itself'
                    })
                category.parent = parent
            except (ValueError, TypeError):
                category.parent = None
        else:
            category.parent = None
        category.save()
        return redirect('dashboard:categories')

    return render(request, 'dashboard/category_edit.html', {
        'category': category,
        'all_categories': all_categories
    })


def users(request):
    res = admin_check(request)
    if res:
        return res
    if request.user.is_superuser is False and request.user.userprofile.role != 'admin':
        return redirect('dashboard:home')
    user_list = User.objects.order_by('username')
    no_admins = []
    for user in user_list:
        if user.is_superuser or user.userprofile.role == 'admin':
            continue
        no_admins.append(user)
    paginator = Paginator(no_admins, 10)
    page = request.GET.get('page')
    users_page = paginator.get_page(page)
    return render(request, 'dashboard/users.html', {'users': users_page})


def user_promote(request, pk):
    res = admin_check(request)
    if res:
        return res

    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.userprofile.role = 'moderator'
        user.userprofile.save()
    return redirect('dashboard:users')

def user_delete(request, pk):
    res = admin_check(request)
    if res:
        return res

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        if not user.is_superuser and user.userprofile.role != 'admin':
            user.delete()
    return redirect('dashboard:users')


def user_demote(request, pk):
    res = admin_check(request)
    if res:
        return res

    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user.userprofile.role == 'moderator':
            user.userprofile.role = 'user'
            user.userprofile.save()
    return redirect('dashboard:users')

def product_create(request):
    res = admin_check(request)
    if res:
        return res

    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST.get('name','').strip()[:50]
            brand = request.POST.get('brand','').strip()[:50]
            price = float(request.POST.get('price',0))
            stock = int(request.POST.get('stock',0))
            category_id = request.POST.get('category')
            if not name or not brand or price < 0 or stock < 0 or not category_id:
                return render(request, 'dashboard/product_edit.html', {'categories': categories, 'error': 'Invalid input'})
            product = Product()
            product.name = name
            product.brand = brand
            product.price = price
            product.stock = stock
            product.description = request.POST.get('description','').strip()[:2000]
            product.category = get_object_or_404(Category, pk=category_id)
            product.featured = 'featured' in request.POST
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            return redirect('dashboard:products')
        except (ValueError, TypeError):
            return render(request, 'dashboard/product_edit.html', {'categories': categories, 'error': 'Invalid input'})

    return render(request, 'dashboard/product_edit.html', {'product': None, 'categories': categories})


def category_create(request):
    res = admin_check(request)
    if res:
        return res

    all_categories = Category.objects.all()
    if request.method == 'POST':
        category = Category()
        category.name = request.POST['name']
        category.bootstrap_icon_code = request.POST['bootstrap_icon_code']
        parent_id = request.POST.get('parent')
        if parent_id:
            category.parent = get_object_or_404(Category, pk=parent_id)
        category.save()
        return redirect('dashboard:categories')

    return render(request, 'dashboard/category_edit.html', {'category': None, 'categories': all_categories})

