from rest_framework import serializers
from .models import *

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['id', 'name']
        
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'name', 'permissions', 'access_admin_panel']
        
class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission']