from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from .services import *
from .permissions import *
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_permission'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_permission'
            
        elif self.action in ['list','retrieve']:
            permission.required_permission = 'view_permission'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_permission'
            
        return [IsAuthenticated(), permission]
    
class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_role'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_role'
            
        elif self.action in ['list','retrieve']:
            permission.required_permission = 'view_permission'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_role'
            
        return [IsAuthenticated(), permission]
    
class RolesPermissionsViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_role_permission'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_role_permission'
            
        elif self.action in ['list','retrieve']:
            permission.required_permission = 'view_role_permission'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_role_permission'
            
        return [IsAuthenticated(), permission]