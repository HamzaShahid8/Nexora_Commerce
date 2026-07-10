from django.contrib import admin
from .models import *


class BaseProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "user",
        "phn_no",
        "address",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "code",
        "user__username",
        "user__email",
        "phn_no",
        "address",
    )
    autocomplete_fields = ("user",)
    readonly_fields = (
        "code",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)

    fieldsets = (
        ("User Information", {
            "fields": ("user",)
        }),
        ("Profile Information", {
            "fields": ("code", "phn_no", "address")
        }),
        ("System Information", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(ManagerProfile)
class ManagerProfileAdmin(BaseProfileAdmin):
    pass


@admin.register(WorkerProfile)
class WorkerProfileAdmin(BaseProfileAdmin):
    pass


@admin.register(CustomerProfile)
class CustomerProfileAdmin(BaseProfileAdmin):
    pass