from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .services import *
from rest_framework.response import Response
from rest_framework import status
from payments.services import *
from payments.models import *
from payments.views import *
from monitoring.models import *
from monitoring.utils import *

# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "payment_status",
        "user",
    ]

    search_fields = [
        "user__username",
        "user__email",
        "shipping_address",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "total_amount",
        "subtotal",
        "status",
    ]

    ordering = [
        "-created_at"
    ]
    

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderReadSerializer
        return OrderWriteSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        queryset = OrderService.get_filtered_orders(self.request.query_params)
        
        if user.role and user.role.name == 'manager':
            return Order.objects.all()
        
        return Order.objects.filter(user = user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            serializer.validated_data,
            request.user
        )
        
        create_log(
            user=self.request.user,
            action='create',
            order=order
        )
        
        payment = order.payment
        
        session = PaymentService.create_checkout_session(payment)

        return Response({
            'order': OrderReadSerializer(order).data,
            'checkout_url': session.url,
        }, status=status.HTTP_200_OK)
        
    def perform_update(self, serializer):
        order = OrderService.update_order(
            serializer.instance,
            serializer.validated_data
        )
        create_log(
            user=self.request.user,
            action='update',
            order=order
        )
        
    def perform_destroy(self, instance):
        create_log(
            user=self.request.uesr,
            action='delete',
            order=instance
        )
        OrderService.delete_order(instance)
        
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_order'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_order'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_order'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_order'
            
        return [IsAuthenticated(), permission]
    
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "order",
        "product",
        "created_by",
    ]

    search_fields = [
        "order__order_number",
        "product__code",
        "product__product__name",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "quantity",
        "price",
        "subtotal",
    ]

    ordering = [
        "-created_at"
    ]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderItemReadSerializer
        return OrderItemWriteSerializer
    
    def get_queryset(self):
        user = self.request.user

        queryset = OrderItemService.get_filtered_order_items(
            self.request.query_params
        )

        if user.role and user.role.name == "manager":
            return queryset

        return queryset.filter(created_by=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        
        if user.role.name == 'manager':
            order_item = serializer.save()
        else:
            order_item = serializer.save(created_by = user)
        create_log(
            user=user,
            action='create',
            order=order_item.order,
            order_item=order_item
        )
        
    def perform_update(self, serializer):
        user = self.request.user
        
        if user.role.name == 'manager':
            order_item = serializer.save()
        else:
            order_item = serializer.save()
        create_log(
            user=user,
            action='update',
            order=order_item.order,
            order_item=order_item
        )
        
    def perform_destroy(self, instance):
        create_log(
            user=self.request.user,
            action='delete',
            order=instance.order,
            order_item=instance
        )
        instance.delete()
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_orderitem'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_orderitem'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_orderitem'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_orderitem'
            
        return [IsAuthenticated(), permission]