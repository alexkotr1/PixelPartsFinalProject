from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('catalogue', views.catalogue, name='catalogue'),
    path('profile/', views.profile, name='profile'),
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)