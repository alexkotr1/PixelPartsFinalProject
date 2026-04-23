from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

ROLES = [
    ('admin', 'Admin'),
    ('moderator', "Moderator"),
    ('user', 'User'),
]


class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    verbose_name = 'Category'
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    bootstrap_icon_code = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    verbose_name = 'Product'
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, blank=True)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLES, default='user')


    class Meta:
        verbose_name_plural = 'User Profiles'
    def __str__(self):
        return self.user.username

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"