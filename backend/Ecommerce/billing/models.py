from django.db import models
import uuid
from django.db.models import Sum
from profiles.models import UUID
from decimal import Decimal


# Create your models here.

class Coupon(models.Model):
    DISCOUNT_TYPE = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed'),
    ]
    code = models.CharField(max_length=100, null=True, blank=True)
    discount_type = models.CharField(max_length=100,choices=DISCOUNT_TYPE, null=True, blank=True)
    discount_value = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=10)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"CPN-{uuid.uuid4().hex[:8].upper()}"
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.code
        
        
class Invoice(UUID):

    INVOICE_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,null=True, related_name='invoices')
    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="invoice"
    )

    payment = models.OneToOneField(
        "payments.Payment",
        on_delete=models.CASCADE,
        related_name="invoice"
    )

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    invoice_number = models.CharField(max_length=100)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="pkr")
    status = models.CharField(
        max_length=20,
        choices=INVOICE_STATUS,
        default="pending"
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = (f"INV-{uuid.uuid4().hex[:8].upper()}")
            
        super().save(*args, **kwargs)
        
    def calculate_totals(self):
        subtotal = self.invoice_items.aggregate(total = Sum('subtotal'))['total'] or 0
        
        self.subtotal = subtotal
        
        self.tax = self.order.tax
        self.shipping_cost = self.order.shipping_cost
        
        self.discount = Decimal('0.00')
        if self.coupon and self.coupon.is_active:
            if self.coupon.discount_type == 'percentage':
                self.discount = (
                    self.subtotal * self.coupon.discount_value
                ) / Decimal('100')
                
            elif self.coupon and self.coupon.discount_type == 'fixed':
                self.discount = self.coupon.discount_value
        
        self.total = (
            self.subtotal + self.tax + self.shipping_cost - self.discount
        )
        
        self.save(update_fields=[
            'subtotal',
            'tax',
            'shipping_cost',
            'discount',
            'total',
        ])
        
        
    def __str__(self):
        return self.invoice_number
        
class InvoiceItem(UUID):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="invoice_items"
    )

    product = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ["-created_at"]
        
    # Calculation
    def save(self, *args, **kwargs):
        
        self.subtotal = self.quantity * self.price
        
        super().save(*args, **kwargs)
        
        self.invoice.calculate_totals()
        
    def __str__(self):
        return self.product.product.name 