from django.db import models
from profiles.models import UUID

# Create your models here.


class Payment(UUID):
    STRIPE_PROVIDER = [
        ('stripe', 'Stripe'),
    ]
    CURRENCY_STATUS = [
        ('usd', 'USD'),
        ('pkr', 'PKR'),
        ('Inr', 'INR')
    ]
    
    PAYMENT_STATUS = [
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='payment')
    provider = models.CharField(max_length=50, choices=STRIPE_PROVIDER, default='stripe')
    payment_intent = models.CharField(max_length=100, unique=True, null=True, blank=True)
    checkout_session_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=30, choices=CURRENCY_STATUS, default='pkr')
    status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default='pending')
    stripe_response = models.JSONField(blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.order.code