from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

# Choices for UserProfile.role
ROLES = [
    ('admin', 'Admin'),
    ('moderator', "Moderator"),
    ('user', 'User'),
]

#Category model
class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    verbose_name = 'Category'
    #self referential foreign key so we can have subcategories
    #on_delete=models.CASCADE means if we delete a category all its subcategories will be deleted as well
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    bootstrap_icon_code = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

#Product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    verbose_name = 'Product'
    #set_null means if a category is deleted products wont get deleted and the category will be set to null
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #PositiveIntegerField prevents negative stock at the db level
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True) #Saved to MEDIA_ROOT/products

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    #OneToOne so only one profile per user
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

#Rating model
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"