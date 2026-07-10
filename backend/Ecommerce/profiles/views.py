from django.shortcuts import render
from .models import *
from accounts.models import *
from roles_permissions.models import *
from rest_framework import viewsets
from .serializers import *
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from monitoring.models import *
from monitoring.utils import *

# Create your views here.


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = ManagerProfile.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    def perform_create(self, serializer):
        if self.request.user.role.name == 'manager':
            manager_profile = serializer.save()
        else:
            manager_profile = serializer.save(user = self.request.user)
            
        create_log(
            user=request.user,
            action='create',
            manager_profile=manager_profile
        )
        
    def perform_update(self, serializer):
        if self.request.user.role.name == 'manager':
            manager_profile = serializer.save()
        else:
            manager_profile = serializer.save(user = self.request.user)
            
        create_log(
            user=request.user,
            action='update',
            manager_profile=manager_profile
        )
        
    def perform_destroy(self, instance):
        create_log(
            user=request.user,
            action='delete',
            manager_profile=instance
        )
        
        instance.delete()
        
        
    def get_queryset(self):
        return ManagerProfile.objects.filter(user=self.request.user)
    
    def get_permissions(self):
        
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_profile'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_profile'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_profile'
            
        elif self.action == 'destory':
            permission.required_permission = 'delete_profile'
            
        return [IsAuthenticated(), permission]
    
class WorkerViewSet(viewsets.ModelViewSet):
    queryset = WorkerProfile.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    def perform_create(self, serializer):
        if self.request.user.role.name == 'manager':
            worker_profile = serializer.save()
        else:
            worker_profile = serializer.save(user = self.request.user)
            
        create_log(
            user=request.user,
            action='create',
            worker_profile=worker_profile
        )
        
    def perform_update(self, serializer):
        if self.request.user.role.name == 'manager':
            worker_profile = serializer.save()
        else:
            worker_profile = serializer.save(user = self.request.user)
            
        create_log(
            user=request.user,
            action='update',
            worker_profile=worker_profile
        )
        
    def perform_destroy(self, instance):
        create_log(
            user=request.user,
            action='delete',
            worker_profile=instance
        )
        instance.delete()
        
    def get_queryset(self):
        if self.request.user.role.name == 'manager':
           return WorkerProfile.objects.all()
        return WorkerProfile.objects.filter(user=self.request.user)
    
    def get_permissions(self):
        
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_profile'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_profile'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_profile'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_profile'
            
        return [IsAuthenticated(), permission]
    
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    def perform_create(self, serializer):
        user = self.request.user
        
        if user.role.name == 'manager':
            customer_profile = serializer.save()
        else:
            customer_profile = serializer.save(user=user)
        
        create_log(
            user=user,
            action='create',
            customer_profile=customer_profile
        )
    
    def perform_update(self, serializer):
        user = self.request.user
        
        if user.role.name == 'manager':
            customer_profile = serializer.save()
        else:
            customer_profile = serializer.save(user=user)
        create_log(
            user=user,
            action='update',
            customer_profile=customer_profile
        )
        
    def perform_destroy(self, instance):
        create_log(
            user=self.request.user,
            action='delete',
            customer_profile=instance
        )
        instance.delete()
        
    def get_queryset(self):
        user = self.request.user
        
        if user.role.name == 'manager':
            return CustomerProfile.objects.all()
        
        return CustomerProfile.objects.filter(user=self.request.user)
    
    def get_permissions(self):
        
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_profile'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_profile'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_profile'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_profile'
            
        return [IsAuthenticated(), permission]