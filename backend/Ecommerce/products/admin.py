from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'created_by')
    search_fields = ("name", 'created_by')
    ordering = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'created_by')
    search_fields = ("name", 'created_by')
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "brand",
        "is_active",
        "created_by"
    )

    list_filter = (
        "category",
        "brand",
        "is_active",
        "created_by"
    )

    search_fields = (
        "name",
        "category__name",
        "brand__name",
        "created_by"
    )

    autocomplete_fields = (
        "category",
        "brand",
    )

    ordering = ("name",)

    fieldsets = (
        ("Product Information", {
            "fields": (
                "name",
                "description",
                "created_by",
            )
        }),
        ("Classification", {
            "fields": (
                "category",
                "brand",
            )
        }),
        ("Status", {
            "fields": (
                "is_active",
            )
        }),
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "sku",
        "price",
        "color",
        "size",
        "created_by",
    )

    list_filter = (
        "color",
        "size",
        "product__category",
        "product__brand",
        "created_by",
    )

    search_fields = (
        "sku",
        "product__name",
    )

    autocomplete_fields = (
        "product",
    )

    readonly_fields = (
        "sku",
    )

    ordering = (
        "product",
        "price",
    )

    fieldsets = (
        ("Product", {
            "fields": (
                "product",
                "image",
            )
        }),
        ("Variant Details", {
            "fields": (
                "sku",
                "price",
                "color",
                "size",
                "created_by",
            )
        }),
    )