from rest_framework import serializers
from .models import *
from accounts.models import *
from accounts.serializers import *
from products.serializers import *

class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductVariantSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['code', 'product', 'quantity', 'price', 'subtotal', 'created_by']
        
class OrderReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemReadSerializer(source="order_item", read_only=True, many=True)
    
    class Meta:
        model = Order
        fields = [
            'code',
            "user",
            "status",
            "payment_status",
            "tax",
            "shipping_cost",
            "discount",
            "shipping_address",
            "subtotal",
            "total_amount",
            "items",
        ]


class OrderItemWriteSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=ProductVariant.objects.all(),
        slug_field="sku"
    )

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity",
        ]


class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(
        many=True,
        write_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "shipping_address",
            "items",
        ]