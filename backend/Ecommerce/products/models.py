from django.db import models
import uuid
from profiles.models import UUID

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Product(UUID):
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand')
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.is_active}"
    
class ProductVariant(UUID):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.sku} - {self.product.name}"