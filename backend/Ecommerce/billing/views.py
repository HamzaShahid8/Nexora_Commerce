from django.shortcuts import render
from .models import *
from .serializers import *
from .services import *
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('order', 'payment', 'coupon').prefetch_related(
        'invoice_items',
        'invoice_items__product',
    )
    
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return InvoiceReadSerializer
        return InvoiceWriteSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        invoice = InvoiceService.create_invoice(
            serializer.validated_data
        )
        
        create_log(
        user=request.user,
        action="create",
        invoice=invoice,
        order=invoice.order,
        payment=invoice.payment,
        )
        
        return Response(
            InvoiceReadSerializer(invoice).data, status=200)
        
    def perform_update(self, serializer):
        InvoiceService.update_invoice(
            serializer.instance,
            serializer.validated_data
        )
        create_log(
        user=self.request.user,
        action="update",
        invoice=invoice,
        order=invoice.order,
        payment=invoice.payment,
        )
        
    def perform_destroy(self, instance):
        create_log(
        user=self.request.user,
        action="delete",
        invoice=instance,
        order=instance.order,
        payment=instance.payment,
        )
        InvoiceService.delete_invoice(instance)
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "currency",
    ]

    search_fields = [
        "invoice_number",
        "order__code",
        "payment__payment_intent",
        "coupon__code",
    ]

    ordering_fields = [
        "created_at",
        "total",
        "subtotal",
    ]
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_bill'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_bill'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_bill'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_bill'
            
        return [IsAuthenticated(), permission]


class InvoiceItemViewSet(viewsets.ModelViewSet):

    queryset = InvoiceItem.objects.select_related(
        "invoice",
        "product",
        "product__product",
        "product__product__category",
        "product__product__brand",
    )

    permission_classes = [
        IsAuthenticated,
        HasPermission,
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "invoice",
        "product",
    ]

    search_fields = [
        "invoice__invoice_number",
        "invoice__order__code",
        "product__sku",
        "product__product__name",
    ]

    ordering_fields = [
        "created_at",
        "quantity",
        "price",
        "subtotal",
    ]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return InvoiceItemReadSerializer

        return InvoiceItemWriteSerializer
    
    def perform_create(self, serializer):
        invoice_item = serializer.save()

        create_log(
            user=self.request.user,
            action="create",
            invoice=invoice_item.invoice,
            invoice_item=invoice_item,
        )
        
    def perform_update(self, serializer):
        invoice_item = serializer.save()

        create_log(
            user=self.request.user,
            action="update",
            invoice=invoice_item.invoice,
            invoice_item=invoice_item,
        )
        
    def perform_destroy(self, instance):
        create_log(
            user=self.request.user,
            action="delete",
            invoice=instance.invoice,
            invoice_item=instance,
        )
 
        instance.delete()
        
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_bill_item'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_bill_item'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_bill_item'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_bill_item'
            
        return [IsAuthenticated(), permission]