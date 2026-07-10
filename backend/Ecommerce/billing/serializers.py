from rest_framework import serializers
from .models import *
from products.serializers import *
from orders.serializers import *
from payments.serializers import *

class CuoponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'is_active']
        read_only_fields = ['code']
        
class InvoiceItemReadSerializer(serializers.ModelSerializer):
    product = ProductVariantSerializer(read_only=True)
    
    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'product', 'quantity', 'price', 'subtotal']
        
class InvoiceReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order = OrderReadSerializer(read_only=True)
    payment = PaymentReadSerializer(read_only=True)
    coupon = CuoponSerializer(read_only=True)
    items = InvoiceItemReadSerializer(source='invoice_items', read_only=True, many=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'user', 'order', 'payment', 'coupon', 'invoice_number', 'subtotal', 'tax', 'shipping_cost', 'discount', 'total', 'currency', 'status', 'items']
        
class InvoiceItemWriteSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(queryset = ProductVariant.objects.all(), slug_field='sku')
    
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity']
        
class InvoiceWriteSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(queryset = Order.objects.all(), slug_field='code')
    payment = serializers.SlugRelatedField(queryset = Payment.objects.all(), slug_field='code')
    coupon = serializers.SlugRelatedField(queryset = Coupon.objects.all(), slug_field='code', allow_null=True, required=False)
    items = InvoiceItemWriteSerializer(source='invoice_items', write_only=True, many=True)
    
    class Meta:
        model = Invoice
        fields = ['order', 'payment', 'coupon', 'items']