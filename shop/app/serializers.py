from django.db.models import Sum
from rest_framework import serializers

from .models import Product, Cart, Order


class ProductsSerializer(serializers.ModelSerializer):


    class Meta:
        model = Product
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["products"]


class OrderSerializer(serializers.ModelSerializer):
    order_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "products", "order_price"]