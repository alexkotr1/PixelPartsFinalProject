from datetime import timedelta

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from cart.models import Purchase
from store.models import Product

# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        return redirect('store:login')

    if request.user.userprofile.role not in ('admin', 'moderator') and not request.user.is_superuser:
        return redirect('store:home')


    last_month = timezone.now() - timedelta(days=30)


    return render(request, 'dashboard/overview.html', {
        'purchases_this_month': Purchase.objects.filter(created_at__gte=last_month).count(),
        'user_count': User.objects.count(),
        'product_count': Product.objects.count(),
        'recent_purchases': Purchase.objects.order_by('-created_at')[:5],
        'featured': Product.objects.all().filter(featured=True)[:4]
    })
