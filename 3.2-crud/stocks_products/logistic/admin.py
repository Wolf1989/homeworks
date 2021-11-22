from django.contrib import admin

from logistic.models import Product, Stock

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass

