from django.contrib import admin
from .models import ActivityLogs


@admin.register(ActivityLogs)
class ActivityLogsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "get_profile",
        "product",
        "order",
        "payment",
        "invoice",
        "timestamp",
    )

    list_display_links = ("id", "user")

    list_filter = (
        "action",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "user__email",
        "product__name",
        "product_variant__sku",
        "order__code",
        "payment__transaction_id",
        "invoice__invoice_number",
    )

    readonly_fields = (
        "timestamp",
    )

    date_hierarchy = "timestamp"

    ordering = ("-timestamp",)

    list_per_page = 25

    autocomplete_fields = (
        "user",
        "manager_profile",
        "worker_profile",
        "customer_profile",
        "product",
        "product_variant",
        "order",
        "order_item",
        "payment",
        "invoice",
        "invoice_item",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "user",
                "manager_profile",
                "worker_profile",
                "customer_profile",
                "product",
                "product_variant",
                "order",
                "order_item",
                "payment",
                "invoice",
                "invoice_item",
            )
        )

    @admin.display(description="Profile")
    def get_profile(self, obj):
        return (
            obj.manager_profile
            or obj.worker_profile
            or obj.customer_profile
            or "-"
        )