from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "order",
        "provider",
        "amount",
        "currency",
        "status",
        "paid_at",
        "created_at",
    )

    list_filter = (
        "provider",
        "status",
        "currency",
        "created_at",
        "paid_at",
    )

    search_fields = (
        "code",
        "order__code",
        "order__user__username",
        "order__user__email",
        "payment_intent",
        "checkout_session_id",
    )

    ordering = (
        "-created_at",
    )

    autocomplete_fields = (
        "order",
    )

    readonly_fields = (
        "code",
        "payment_intent",
        "checkout_session_id",
        "stripe_response",
        "paid_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "order",
                    "provider",
                    "status",
                )
            },
        ),
        (
            "Payment Details",
            {
                "fields": (
                    "amount",
                    "currency",
                    "payment_intent",
                    "checkout_session_id",
                    "paid_at",
                )
            },
        ),
        (
            "Stripe Response",
            {
                "fields": (
                    "stripe_response",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "code",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )