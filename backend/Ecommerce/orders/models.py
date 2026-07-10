from django.db import models
from accounts.models import BaseModel
from profiles.models import UUID
from django.db.models import Sum

# Create your models here.

class Order(UUID):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='order')
    status = models.CharField(max_length=100, choices=ORDER_STATUS, blank=True, null=True, default='pending')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=100, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2, default=250,  blank=True, null=True)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=300, blank=True, null=True)
    shipping_address = models.CharField(max_length=200, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def calculate_totals(self):
        subtotal = self.order_item.aggregate(total=Sum('subtotal'))['total'] or 0
        
        self.subtotal = subtotal
        self.total_amount = subtotal + (self.tax) + (self.shipping_cost) - (self.discount)
        
        self.save()
        
    def __str__(self):
        return (self.code) if self.code else f"{self.id}"
    
class OrderItem(UUID):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE, related_name='order_item')
    quantity = models.PositiveIntegerField(default = 0)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.product} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)
        
        self.order.calculate_totals()