from django.contrib import admin
from .models import Coupon, Invoice, InvoiceItem


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "discount_type",
        "discount_value",
        "is_active",
    )

    list_filter = (
        "discount_type",
        "is_active",
    )

    search_fields = (
        "code",
    )

    readonly_fields = (
        "code",
    )

    fieldsets = (
        (
            "Coupon Information",
            {
                "fields": (
                    "code",
                    "discount_type",
                    "discount_value",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "user",
        "order",
        "payment",
        "coupon",
        "subtotal",
        "discount",
        "total",
        "currency",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "currency",
        "created_at",
    )

    search_fields = (
        "invoice_number",
        "user__username",
        "user__email",
        "order__code",
        "payment__payment_intent",
        "coupon__code",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "subtotal",
        "tax",
        "shipping_cost",
        "discount",
        "total",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "user",
        "order",
        "payment",
        "coupon",
    )

    fieldsets = (
        (
            "Invoice Information",
            {
                "fields": (
                    "invoice_number",
                    "user",
                    "order",
                    "payment",
                    "coupon",
                ),
            },
        ),
        (
            "Billing Summary",
            {
                "fields": (
                    "subtotal",
                    "tax",
                    "shipping_cost",
                    "discount",
                    "total",
                    "currency",
                    "status",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):

    list_display = (
        "invoice",
        "product",
        "quantity",
        "price",
        "subtotal",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "invoice__invoice_number",
        "product__sku",
        "product__product__name",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "price",
        "subtotal",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "invoice",
        "product",
    )

    fieldsets = (
        (
            "Invoice Item",
            {
                "fields": (
                    "invoice",
                    "product",
                    "quantity",
                ),
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "price",
                    "subtotal",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )