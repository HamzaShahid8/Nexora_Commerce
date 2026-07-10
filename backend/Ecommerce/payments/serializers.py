from rest_framework import serializers
from .models import *
from orders.serializers import *

class PaymentReadSerializer(serializers.ModelSerializer):
    order = OrderReadSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['code', "order",  "provider", "payment_intent", "checkout_session_id", "amount", "currency", "status", "paid_at", "created_at",]
        
class PaymentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "order",
            "provider",
            "amount",
            "currency",
        ]
        read_only_fields = [
            "provider",
        ]

class CheckoutSerializer(serializers.Serializer):
    payment_code = serializers.CharField()