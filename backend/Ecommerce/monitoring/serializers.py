from .models import *
from rest_framework import serializers


class ActivityLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLogs
        fields = [
            'id',
            'user',
            'action',
            'manager_profile',
            'worker_profile',
            'customer_profile',
            'product',
            'product_variant',
            'order',
            'order_item',
            'payment',
            'invoice',
            'invoice_item',
            'timestamp',
        ]