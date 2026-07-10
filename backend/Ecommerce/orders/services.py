from django.db import transaction
from django.db.models import Q
from payments.models import Payment
from .models import Order, OrderItem

class OrderService:

    @staticmethod
    def get_filtered_orders(query_params):

        queryset = Order.objects.select_related("user")

        # Query Params 
        status = query_params.get("status")
        payment_status = query_params.get("payment_status")
        user = query_params.get("user")
        search = query_params.get("search")
        min_total = query_params.get("min_total")
        max_total = query_params.get("max_total")
        created_after = query_params.get("created_after")
        created_before = query_params.get("created_before")
        ordering = query_params.get("ordering")

        # Status Filter
        if status:
            queryset = queryset.filter(status=status)

        # Payment Status Filter
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)

        # User Filter
        if user:
            queryset = queryset.filter(user__id=user)

        # Search Filter
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )

        # Total Filters
        if min_total:
            queryset = queryset.filter(total_amount__gte=min_total)

        if max_total:
            queryset = queryset.filter(total_amount__lte=max_total)

        # Date Filters
        if created_after:
            queryset = queryset.filter(created_at__date__gte=created_after)

        if created_before:
            queryset = queryset.filter(created_at__date__lte=created_before)

        # Ordering 
        allowed_ordering = [
            "created_at",
            "-created_at",
            "total_amount",
            "-total_amount",
        ]

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    @staticmethod
    @transaction.atomic
    def create_order(validated_data, user):

        items = validated_data.pop("items")

        order = Order.objects.create(
            user=user,
            **validated_data
        )

        for item in items:

            product = item["product"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=product.price,
                created_by=user,
            )

        order.calculate_totals()

        Payment.objects.create(
            order=order,
            amount=order.total_amount,
        )

        return order

    @staticmethod
    @transaction.atomic
    def bulk_create_order(validated_data, user):

        items = validated_data.pop("items")

        order = Order.objects.create(
            user=user,
            created_by=user,
            **validated_data
        )

        order_items = []

        for item in items:

            product = item["product"]
            quantity = item["quantity"]
            price = product.price

            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price,
                    subtotal=price * quantity,
                    created_by=user,
                )
            )

        OrderItem.objects.bulk_create(order_items)

        order.calculate_totals()

        Payment.objects.create(
            order=order,
            amount=order.total_amount,
        )

        return order

    @staticmethod
    @transaction.atomic
    def update_order(instance, validated_data):

        items = validated_data.pop("items", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if items is not None:

            instance.order_item.all().delete()

            for item in items:

                OrderItem.objects.create(
                    order=instance,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price,
                    created_by=instance.created_by,
                )

        instance.calculate_totals()

        return instance

    @staticmethod
    @transaction.atomic
    def delete_order(instance):

        instance.delete()

        return True


class OrderItemService:

    @staticmethod
    def get_filtered_order_items(query_params):

        queryset = OrderItem.objects.select_related(
            "order",
            "product",
            "product__product",
            "created_by",
        )

        # Query Params
        order = query_params.get("order")
        product = query_params.get("product")
        created_by = query_params.get("created_by")
        search = query_params.get("search")
        ordering = query_params.get("ordering")

        # Order Filter
        if order:
            queryset = queryset.filter(order__id=order)

        # Product Filter
        if product:
            queryset = queryset.filter(product__id=product)

        # Created By Filter
        if created_by:
            queryset = queryset.filter(created_by__id=created_by)

        # Search Filter
        if search:
            queryset = queryset.filter(
                Q(product__sku__icontains=search) |
                Q(product__product__name__icontains=search)
            )

        # Ordering
        allowed_ordering = [
            "created_at",
            "-created_at",
            "subtotal",
            "-subtotal",
        ]

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-created_at")

        return queryset