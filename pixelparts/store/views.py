from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RegisterForm
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
    form = RegisterForm(request.POST, request.FILES)
    if form.is_valid():
        user = form.save()
        UserProfile.objects.create(user=user,
                                   date_of_birth=form.cleaned_data['date_of_birth'],
                                   avatar=form.cleaned_data['avatar'],
                                   phone=form.cleaned_data['phone'],
                                   address=form.cleaned_data['address'],
                                   city=form.cleaned_data['city'],
                                   country=form.cleaned_data['country'],
        )
        user.save()
        login(request, user)
        return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

