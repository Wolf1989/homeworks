from itertools import product
from django.db.models import fields
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта

    class Meta:
        model = Product
        fields = "__all__"


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    quantity = serializers.IntegerField(min_value=0, default=1)
    price = serializers.FloatField(min_value=0.1, default=0.1)
    product = PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=True
    )

    class Meta:
        model = StockProduct
        fields = ('id', 'product', 'quantity', 'price')


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ('id', 'address', 'positions')

    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада
    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            product = position.pop('product')
            stock.products.add(product, through_defaults=position)
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions', None)

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        if positions:
            for position in positions:
                product = position.pop('product')
                StockProduct.objects.update_or_create(
                    stock=stock, product=product, defaults=dict(position)
                )

        return stock
