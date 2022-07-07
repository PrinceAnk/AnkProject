from itertools import product
from django.db import models

from seller.models import Product

# Create your models here.

class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return self.product.name

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_status=models.CharField(max_length=50)

    def __str__(self):
        return self.user.name

class OrderDetails(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    order=models.ForeignKey(Order,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name