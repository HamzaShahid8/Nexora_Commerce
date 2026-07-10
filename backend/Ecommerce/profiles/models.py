from django.db import models
from accounts.models import *
import uuid

# Create your models here.

class UUID(BaseModel):
    code = models.CharField(max_length=100, null=True, blank=True, unique=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"DES-{uuid.uuid4().hex[:8].upper()}"
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.code

class ManagerProfile(UUID):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    phn_no = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.phn_no} - {self.address}"
    

class WorkerProfile(UUID):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    phn_no = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.phn_no} - {self.address}"
    

class CustomerProfile(UUID):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    phn_no = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.phn_no} - {self.address}"