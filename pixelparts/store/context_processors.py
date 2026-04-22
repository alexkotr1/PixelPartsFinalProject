from .models import Category

def footer_categories(request):
    return {'footer_categories': Category.objects.filter(parent=None)[:5]}