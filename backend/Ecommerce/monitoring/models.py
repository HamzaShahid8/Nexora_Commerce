from django.db import models
from accounts.models import *
from profiles.models import *
from roles_permissions.models import *
from orders.models import *
from payments.models import *
from products.models import *
from billing.models import *

# Create your models here.

class ActivityLogs(models.Model):
    ACTION_STATUS = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs', null=True, blank=True)
    action = models.CharField(max_length=100, choices=ACTION_STATUS, null=True, blank=True)
    manager_profile = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE, related_name='activity_logs', blank=True, null=True)
    worker_profile = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name='activity_logs', blank=True, null=True)
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='activity_logs', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='activity_logs', blank=True, null=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='activity_logs', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='activity_logs', blank=True, null=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='activity_logs', blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='activity_logs',blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='activity_logs', blank=True, null=True)
    invoice_item = models.ForeignKey(InvoiceItem, on_delete=models.CASCADE, related_name='activity_logs', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']
        
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"