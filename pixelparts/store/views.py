from django.shortcuts import render
from .models import Product
# Create your views here.

def home(request):
    featured = Product.objects.all().filter(featured=True)[:4]
    return render(request, 'store/home.html', {'featured': featured})