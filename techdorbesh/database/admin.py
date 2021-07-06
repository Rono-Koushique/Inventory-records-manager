from django.contrib import admin
from .models import Product, Sell, Order

# Register your models here.

admin.site.register(Product)
admin.site.register(Sell)
admin.site.register(Order)