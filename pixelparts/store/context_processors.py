from .models import Category

def footer_categories(request):
    #inject categories into every template for the footer
    return {'footer_categories': Category.objects.filter(parent=None)[:5]}