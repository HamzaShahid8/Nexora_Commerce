from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = [
        "subtotal",
        "created_by",
        "created_at",
        "updated_at",
    ]

    fields = [
        'id',
        "product",
        "quantity",
        "price",
        "subtotal",
        "created_by",
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        "user",
        "status",
        "payment_status",
        "subtotal",
        "total_amount",
        "created_at",
    ]

    list_filter = [
        'id',
        "status",
        "payment_status",
        "created_at",
    ]

    search_fields = [
        'id',
        "user__username",
        "user__email",
    ]

    readonly_fields = [
        "subtotal",
        "total_amount",
        "created_at",
        "updated_at",
    ]

    fieldsets = (

        ("Order Information", {
            "fields": (
                "user",
                "status",
                "payment_status",
            )
        }),

        ("Pricing Details", {
            "fields": (
                "subtotal",
                "tax",
                "shipping_cost",
                "discount",
                "total_amount",
            )
        }),

        ("Shipping Information", {
            "fields": (
                "shipping_address",
            )
        }),

        ("Audit Information", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    inlines = [
        OrderItemInline
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        "order",
        "product",
        "quantity",
        "price",
        "subtotal",
        "created_at",
    ]

    list_filter = [
        'id',
        "created_at",
    ]

    search_fields = [
        'id',
        "order",
        "product__code",
        "product__product__name",
    ]

    readonly_fields = [
        "subtotal",
        "created_at",
        "updated_at",
    ]

    fieldsets = (

        ("Order Item Details", {
            "fields": (
                'id',
                "order",
                "product",
                "quantity",
                "price",
                "subtotal",
            )
        }),

        ("Audit Information", {
            "fields": (
                "created_by",
                "created_at",
                "updated_at",
            )
        }),

    )