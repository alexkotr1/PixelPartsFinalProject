from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.



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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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

