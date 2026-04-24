from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from cart.models import Purchase
from store.models import Product, Category, UserProfile

import json
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

    product_list = Product.objects.order_by('-featured','name') #- is descending order so true goes first
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'dashboard/products.html', {'products': products_page})


def admin_check(request):
    if not request.user.is_authenticated:
        return redirect('store:login')
    if not request.user.is_superuser and get_role(request.user) not in ('admin', 'moderator'):
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
    categories = Category.objects.all()
    if request.method == 'POST':
        validation, product = validate_product(request, pk)
        if not validation:
            product = get_object_or_404(Product, pk=pk)
            return render(request, 'dashboard/product_edit.html', {
                'product': product,
                'categories': categories,
                'error': 'Invalid input',
            })
        return redirect('dashboard:products')

    product = get_object_or_404(Product, pk=pk)
    return render(request, 'dashboard/product_edit.html', {
        'product': product,
        'categories': categories,
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
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name','').strip()[:50]
        icon = request.POST.get('bootstrap_icon_code','').strip()[:50]

        if not name:
            return render(request, 'dashboard/category_edit.html', {
                'category': category,
                'categories': categories,
                'error': 'Name is required',
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
                        'categories': categories,
                        'error': 'A category cannot be a parent of itself',
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
        'categories': categories,
    })


def users(request):
    res = admin_check(request)
    if res:
        return res
    if not request.user.is_superuser and get_role(request.user) != 'admin':
        return redirect('store:home')
    user_list = User.objects.order_by('username')
    no_admins = []
    for user in user_list:
        if user.is_superuser or get_role(user) == 'admin':
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
    if not request.user.is_superuser and get_role(request.user) != 'admin':
        return redirect('dashboard:overview')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = 'moderator'
        profile.save()
    return redirect('dashboard:users')

def user_delete(request, pk):
    res = admin_check(request)
    if res:
        return res

    user = get_object_or_404(User, pk=pk)
    if user.pk == request.user.pk:
        return redirect('dashboard:users')
    if request.method == 'POST':
        if not user.is_superuser and get_role(user) != 'admin':
            user.delete()
    return redirect('dashboard:users')


def user_demote(request, pk):
    res = admin_check(request)
    if res:
        return res
    if not request.user.is_superuser and get_role(request.user) != 'admin':
        return redirect('dashboard:overview')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if get_role(user) == 'moderator':
            user.userprofile.role = 'user'
            user.userprofile.save()
    return redirect('dashboard:users')

def product_create(request):
    res = admin_check(request)
    if res:
        return res

    categories = Category.objects.all()
    if request.method == 'POST':
        validation, product = validate_product(request, None)
        if not validation:
            return render(request, 'dashboard/product_edit.html', {
                'product': None,
                'categories': categories,
                'error': 'Invalid input',
            })
        return redirect('dashboard:products')

    return render(request, 'dashboard/product_edit.html', {
        'product': None,
        'categories': categories,
    })


def category_create(request):
    res = admin_check(request)
    if res:
        return res

    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()[:50]
        icon = request.POST.get('bootstrap_icon_code', '').strip()[:50]

        if not name:
            return render(request, 'dashboard/category_edit.html', {
                'category': None,
                'categories': categories,
                'error': 'Name is required',
            })

        category = Category(name=name, bootstrap_icon_code=icon)
        parent_id = request.POST.get('parent')
        if parent_id:
            category.parent = get_object_or_404(Category, pk=parent_id)
        category.save()
        return redirect('dashboard:categories')

    return render(request, 'dashboard/category_edit.html', {
        'category': None,
        'categories': categories,
    })


def bulk_import(request):
    res = admin_check(request)
    if res:
        return res
    if request.method != "POST":
        return redirect('dashboard:products')
    import_file = request.FILES.get("file")
    if import_file is None:
        return JsonResponse({"error": "no file"})
    try:
        data = json.load(import_file)
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid json"})
    counter = 0
    try:
        for item in data:
            counter += 1
            name = item.get('name')
            brand = item.get('brand')
            price = item.get('price',0)
            stock = item.get('stock',0)
            category_id = item.get('category')
            featured = item.get('featured')
            description = item.get('description','')
            res, product = validate_product(None, None, name, brand, price, stock, description, category_id, featured)
            if not res:
                return JsonResponse({"error": f"Error validating product #{counter}: {product.name}"})
            product.save()
    except Exception as e:
        return JsonResponse({"error": f"Error validating product #{counter}: {e}"})
    return JsonResponse({"success": True})

def validate_product(request, pk, name_=None, brand_=None, price_=None, stock_=None, description_=None, category_id_=None,featured_=None):
    product = None
    if pk:
         product = get_object_or_404(Product, pk=pk)
    try:
        name = (name_ if name_ else (request.POST.get('name','')).strip()[:50] if request else '')
        brand = (brand_ if brand_ else (request.POST.get('brand',"")).strip()[:50] if request else '')
        price = float(price_ if price_ else (request.POST.get('price',0)) if request else 0)
        stock = int(stock_ if stock_ else (request.POST.get('stock',0)) if request else 0)
        description = description_ if description_ else (request.POST.get('description','').strip()[:2000] if request else '')
        category_id = category_id_ if category_id_ else (request.POST.get("category") if request else '')
        if not name or not brand or price < 0 or stock < 0 or not category_id:
            return False, None
        category = Category.objects.get(pk=category_id)
    except (ValueError, TypeError, ObjectDoesNotExist):
        return False, None
    if not pk: product = Product()
    product.name = name
    product.brand = brand
    product.price = price
    product.stock = stock
    product.description = description
    product.category = category
    product.featured = featured_ if featured_ else ('featured' in request.POST if request else False)
    if request:
        if pk and 'delete_image' in request.POST and product.image:
            product.image.delete(save=False)
            product.image = None

        if 'image' in request.FILES:
            product.image = request.FILES['image']
    try:
        product.save()
    except (IntegrityError, ValueError):
        return False, None

    return True, product


def get_role(user):
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    return userprofile.role
