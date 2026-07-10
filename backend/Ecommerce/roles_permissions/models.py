from django.db import models

# Create your models here.

class Permissions(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.name
    
class Roles(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    permissions = models.ManyToManyField(Permissions)
    access_admin_panel = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name}"
    
class RolePermission(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True)
    permission = models.ForeignKey(Permissions, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.role} - {self.permission}"