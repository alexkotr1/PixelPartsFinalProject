from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RegisterForm, ProfileEditForm
from .models import Product, Category, UserProfile, Rating
from cart.models import Purchase
from django.core.paginator import Paginator


# Create your views here.


def home(request):
    featured = Product.objects.all().filter(featured=True)[:4]
    featured_with_images = []
    for product in featured:
        if product.image:
            featured_with_images.append(product)
    return render(request, 'store/home.html', {'featured': featured_with_images, 'categories': Category.objects.all()[:8]})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ratings = Rating.objects.filter(product=product)
    user_rating = 0
    total = 0
    for r in ratings:
        total += r.rating
        if request.user.is_authenticated and r.user_id == request.user.id:
            user_rating = r.rating
    count = ratings.count()
    avg = total / count if count > 0 else 0
    return render(request, 'store/product_detail.html', {
        'product': product,
        'average': int(round(avg, 1)),
        'count': count,
        'user_rating': int(user_rating),
    })

@login_required
def rate_product(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=400)
    product = get_object_or_404(Product, pk=pk)
    value = int(request.POST.get('rating'))
    if value not in range(1, 6):
        return JsonResponse({'error': 'Invalid rating'}, status=400)
    rating,created = Rating.objects.get_or_create(product=product, user=request.user,defaults={'rating': value})
    if not created:
        rating.rating = value
        rating.save()
    sum = 0
    ratings = Rating.objects.filter(product=product)
    for rating2 in ratings:
        sum += rating2.rating
    avg = sum / ratings.count() if ratings.count() > 0 else 0
    print(round(avg,1),ratings.count(),int(value))
    return JsonResponse({
        'average':int(round(avg,1)),
        'count':ratings.count(),
        'user_rating':int(value),
    })





def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user,
                                       date_of_birth=form.cleaned_data.get('date_of_birth'),
                                       avatar=form.cleaned_data.get('avatar'),
                                       phone=form.cleaned_data.get('phone', ''),
                                       address=form.cleaned_data.get('address', ''),
                                       city=form.cleaned_data.get('city', ''),
                                       country=form.cleaned_data.get('country', ''),
            )
            user.save()
            login(request, user)
            return redirect('store:home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})


def catalogue(request):
    category_id = request.GET.get('category')
    searched = request.GET.get('search_text')
    brand = request.GET.get('brand')
    price_start = request.GET.get('price_start')
    price_end = request.GET.get('price_end')
    selected_category = None
    parent_category = None
    subcategories = []
    products = Product.objects.all()

    if category_id:
        category_id = int(category_id)
        selected_category = get_object_or_404(Category, pk=category_id)
        subcategory_ids = list(Category.objects.filter(parent_id=category_id).values_list('id', flat=True))
        products = products.filter(category_id__in=[category_id] + subcategory_ids)

        if selected_category.parent:
            subcategories = Category.objects.filter(parent=selected_category.parent)
            parent_category = selected_category.parent
        else:
            subcategories = Category.objects.filter(parent_id=category_id)
            parent_category = selected_category

    if brand:
        products = products.filter(brand=brand)

    if price_start:
        products = products.filter(price__gte=price_start)
    if price_end:
        products = products.filter(price__lte=price_end)

    if searched:
        hits = []
        for product in products:
            search_terms = searched.lower().strip().split(" ")
            if searched.lower() in product.name.lower() or searched.lower() in product.brand.lower():
                hits.append(product)

            elif len(search_terms) > 0:
                for term in search_terms:
                    if term in product.name.lower() or term in product.brand.lower() and product not in hits:
                        hits.append(product)

        products = hits

    top_categories = Category.objects.filter(parent=None)
    brands = Product.objects.values_list('brand', flat=True).distinct()

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    query_string = query_params.urlencode()

    return render(request, 'store/catalogue.html', {
        'products': products_page,
        'top_categories': top_categories,
        'subcategories': subcategories,
        'selected_category': selected_category,
        'selected_category_id': category_id,
        'parent_category': parent_category if category_id else None,
        'search_text': "" if (searched and searched == "") or searched is None else searched,
        'price_start': price_start,
        'price_end': price_end,
        'brand': brand,
        'brands': brands,
        'query_string': query_string,

    })

@login_required
def profile(request):
    user = request.user
    user_profile,created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            if request.POST.get('delete_avatar'):
                user_profile.avatar.delete(save=True)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()
            return redirect('store:profile')
    else:
        form = ProfileEditForm(instance=user_profile, initial={'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name})

    return render(request, 'store/profile.html', {'form': form, 'user_profile': user_profile})

@login_required
def user_dashboard(request):
    purchase_list = Purchase.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(purchase_list, 5)
    page = request.GET.get('page')
    purchases = paginator.get_page(page)
    return render(request, 'store/user_dashboard.html', {'purchases': purchases})



