from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.created_at) + " - " + str(self.total)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.product) + " - " + str(self.quantity) + " [" + str(self.purchase) + "]"
