from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets
from .models import *
from rest_framework.permissions import IsAuthenticated
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .services import *
from monitoring.models import *
from monitoring.utils import *

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)
    
    def get_permissions(self):
        
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_category'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_category'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_category'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_category'
            
        return [IsAuthenticated(), permission]
    
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)
    
    def get_permissions(self):
        
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_brand'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_brand'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_brand'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_brand'
            
        return [IsAuthenticated(), permission]
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_queryset(self):
        return ProductService.get_filtered_products(self.request.query_params)
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role.name == 'manager':
            product = serializer.save()
        else:
            product = serializer.save(created_by = user)
            
        create_log(
            user=user,
            action='create',
            product=product
        )
        
    def perform_update(self, serializer):
        user = self.request.user
        
        if user.role.name == 'manager':
            product = serializer.save()
        else:
            product = serializer.save()
            
        create_log(
            user=user,
            action='update',
            product=product
        )
        
    def perform_destroy(self, instance):
        create_log(
            user=self.request.user,
            action='delete',
            product=instance
        )
        instance.delete()

    def get_permissions(self):
        
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_product'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_product'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_product'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_product'
            
        return [IsAuthenticated(), permission]
    
class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['id', 'sku', 'product__name', 'price', 'color', 'size']
    
    search_fields = ['id', 'sku', 'product__name', 'size', 'color']
    
    ordering_fields = ['id', 'sku', 'product__name', 'color', 'size']
    
    def get_queryset(self):
        return ProductVariantService.get_filtered_variants(self.request.query_params)
     
    def perform_create(self, serializer):
        user = self.request.user
        
        if user.role.name == 'manager':
            product_variant = serializer.save()
        else:
            product_variant = serializer.save(created_by = user)
            
        create_log(
            user=user,
            action='create',
            product=product_variant.product,
            product_variant=product_variant
        )
        
    def perform_update(self, serializer):
        user = self.request.user
        
        if user.role.name == 'manager':
            product_variant = serializer.save()
        else:
            product_variant = serializer.save()
        create_log(
            user=user,
            action='update',
            product=product_variant.product,
            product_variant=product_variant
        )
    
    def get_permissions(self):
        
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_product_variant'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_product_variant'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_product_variant'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_product_variant'
            
        return [IsAuthenticated(), permission]
    
    def perform_destroy(self, instance):
        create_log(
            user=self.request.user,
            action='delete',
            product=instance.product,
            product_variant=instance
        )
        instance.delete()
        
        delete_product_variant(instance)