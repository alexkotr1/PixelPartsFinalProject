from django.shortcuts import render, get_object_or_404
from .models import Product, Category
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