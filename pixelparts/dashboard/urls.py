from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.overview, name='home'),
    path('products/', views.products, name='products'),
    path('product_delete:<int:pk>/', views.product_delete, name='product_delete'),
    path('product_edit:<int:pk>/', views.product_edit, name='product_edit'),
    path('product_create/', views.product_create, name='product_create'),

    path('categories/', views.categories, name='categories'),
    path('category_delete:<int:pk>/', views.category_delete, name='category_delete'),
    path('category_edit:<int:pk>/', views.category_edit, name='category_edit'),
    path('category_create/', views.category_create, name='category_create'),

    path('users/', views.users, name='users'),
    path('user_promote:<int:pk>/', views.user_promote, name='user_promote'),
    path('user_delete:<int:pk>/', views.user_delete, name='user_delete'),
    path('user_demote:<int:pk>/', views.user_demote, name='user_demote'),

]