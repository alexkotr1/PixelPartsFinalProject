from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RegisterForm, ProfileEditForm
from .models import Product, Category, UserProfile


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
    return render(request, 'store/product_detail.html', {'product': product})

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
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})


def catalogue(request):
    category_id = request.GET.get('category')
    searched = request.GET.get('search_text')
    brand = request.GET.get('brand')
    price_start = request.GET.get('price_start')
    price_end = request.GET.get('price_end')

    products = Product.objects.all()

    if category_id:
        category_id = int(category_id)
        products = products.filter(category_id=category_id)

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

    categories = Category.objects.all()
    brands = Product.objects.values_list('brand', flat=True).distinct()
    print(list(brands))

    return render(request, 'store/catalogue.html', {
        'products': products,
        'categories': categories,
        'selected_category_id': category_id,
        'search_text': "" if (searched and searched == "") or searched is None else searched,
        'price_start': price_start,
        'price_end': price_end,
        'brand': brand,
        'brands': brands,

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
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=user_profile, initial={'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name})

    return render(request, 'store/profile.html', {'form': form, 'user_profile': user_profile})


