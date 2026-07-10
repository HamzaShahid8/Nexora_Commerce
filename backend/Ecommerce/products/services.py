from .models import *

from django.db.models import Q
from .models import Product, ProductVariant


class ProductService:

    @staticmethod
    def get_filtered_products(query_params):

        queryset = Product.objects.select_related(
            "category",
            "brand",
            "created_by",
        )

        # Query Params
        category = query_params.get("category")
        brand = query_params.get("brand")
        is_active = query_params.get("is_active")
        created_by = query_params.get("created_by")
        search = query_params.get("search")
        ordering = query_params.get("ordering")

        # Category Filter
        if category:
            queryset = queryset.filter(category__id=category)

        # Brand Filter
        if brand:
            queryset = queryset.filter(brand__id=brand)

        # Active Filter
        if is_active:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        # Created By Filter
        if created_by:
            queryset = queryset.filter(created_by__id=created_by)

        # Search Filter
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search) |
                Q(brand__name__icontains=search)
            )

        # Ordering
        allowed_ordering = [
            "name",
            "-name",
            "created_at",
            "-created_at",
        ]

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-created_at")

        return queryset


class ProductVariantService:

    @staticmethod
    def get_filtered_variants(query_params):

        queryset = ProductVariant.objects.select_related(
            "product",
            "product__category",
            "product__brand",
            "created_by",
        )

        # Query Params
        product = query_params.get("product")
        category = query_params.get("category")
        brand = query_params.get("brand")
        sku = query_params.get("sku")
        color = query_params.get("color")
        size = query_params.get("size")
        min_price = query_params.get("min_price")
        max_price = query_params.get("max_price")
        created_by = query_params.get("created_by")
        search = query_params.get("search")
        ordering = query_params.get("ordering")

        # Product Filter
        if product:
            queryset = queryset.filter(product__id=product)

        # Category Filter
        if category:
            queryset = queryset.filter(product__category__id=category)

        # Brand Filter
        if brand:
            queryset = queryset.filter(product__brand__id=brand)

        # SKU Filter
        if sku:
            queryset = queryset.filter(sku__icontains=sku)

        # Color Filter
        if color:
            queryset = queryset.filter(color__iexact=color)

        # Size Filter
        if size:
            queryset = queryset.filter(size__iexact=size)

        # Price Filters
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Created By Filter
        if created_by:
            queryset = queryset.filter(created_by__id=created_by)

        # Search Filter
        if search:
            queryset = queryset.filter(
                Q(product__name__icontains=search) |
                Q(product__category__name__icontains=search) |
                Q(product__brand__name__icontains=search) |
                Q(sku__icontains=search) |
                Q(color__icontains=search) |
                Q(size__icontains=search)
            )

        # Ordering
        allowed_ordering = [
            "price",
            "-price",
            "sku",
            "-sku",
            "created_at",
            "-created_at",
        ]

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-created_at")

        return queryset


def create_product_variant(validated_data):

    product_data = validated_data.pop("product")

    category_data = product_data.pop("category")
    brand_data = product_data.pop("brand")

    category, _ = Category.objects.get_or_create(**category_data)
    brand, _ = Brand.objects.get_or_create(**brand_data)

    product_data["category"] = category
    product_data["brand"] = brand

    product, _ = Product.objects.get_or_create(**product_data)

    validated_data["product"] = product

    return ProductVariant.objects.create(**validated_data)


def update_product_variant(instance, validated_data):

    product_data = validated_data.pop("product")

    category_data = product_data.pop("category")
    brand_data = product_data.pop("brand")

    category, _ = Category.objects.get_or_create(**category_data)
    brand, _ = Brand.objects.get_or_create(**brand_data)

    product = instance.product
    product.name = product_data.get("name", product.name)
    product.description = product_data.get("description", product.description)
    product.is_active = product_data.get("is_active", product.is_active)
    product.category = category
    product.brand = brand
    product.save()

    instance.image = validated_data.get("image", instance.image)
    instance.price = validated_data.get("price", instance.price)
    instance.color = validated_data.get("color", instance.color)
    instance.size = validated_data.get("size", instance.size)
    instance.save()

    return instance


def delete_product_variant(instance):

    product = instance.product

    instance.delete()

    if not ProductVariant.objects.filter(product=product).exists():
        product.delete()