from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.utils import timezone
from django.contrib.auth.models import Group
from roles_permissions.models import Roles
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    role = models.ForeignKey('roles_permissions.Roles', on_delete=models.SET_NULL, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username} - {self.email}"
    
    
    # access admin panel
    def save(self, *args, **kwargs):
        
        # automatic access admin panel based on role
        if self.role and self.role.name.lower() == 'manager':
            self.is_staff = True
            self.is_superuser = False
            
        else:
            self.is_staff = False
            self.is_superuser = False
            
        super().save(*args, **kwargs)
        
        # sync role to django group
        if self.role:
            group, _ = Group.objects.get_or_create(name=self.role.name)
            
            self.groups.set([group])
            
        else:
            self.groups.clear()

    def __str__(self):
        return self.email or self.username
    
class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = str(random.randint(100000, 999999))
            
        if not self.expires_at:
            self.expires_at = timezone.now() - timezone.timedelta(minutes=5)
            
        super().save(*args, **kwargs)