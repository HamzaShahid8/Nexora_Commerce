from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'password', 'image', 'role')
    search_fields = ('id', 'username', 'email', 'role')
    
    def save_model(self, request, obj, form, change):
        if not change:  # new user create horha h 
            obj.set_password(obj.password) # obj -> jo save hua h abhi
        super().save_model(request, obj, form, change)
    
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'otp', 'email', 'is_verified', 'expires_at', 'created_at')
    search_fields = ('id', 'email', 'is_verified', 'created_at')