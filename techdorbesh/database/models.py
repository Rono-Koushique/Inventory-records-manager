from django.db import models
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, null=True)
    unit = models.CharField(max_length=20, null=True)
    quantity = models.PositiveIntegerField(null=True)
    priceBuy = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name} - {self.quantity}'

class Sell(models.Model):
    cusName = models.CharField(max_length=100, null=True)
    cusContact = models.CharField(max_length=20, null=True)
    cusAddress = models.CharField(max_length=200, null=True)
    cusEmail = models.EmailField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(null=True)
    def __str__(self):
        return f'{self.date}'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField()
    price_buy = models.IntegerField(null=True)
    price_sell = models.IntegerField(null=True)
    price_total = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.product} - {self.order_quantity}'