from django.contrib import admin
from .models import *


class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1
    autocomplete_fields = ["permission"]


@admin.register(Permissions)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Roles)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        'access_admin_panel',
    )
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ("permissions",)
    inlines = [RolePermissionInline]


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "role",
        "permission",
    )
    list_filter = (
        "role",
        "permission",
    )
    search_fields = (
        "role__name",
        "permission__name",
    )
    autocomplete_fields = (
        "role",
        "permission",
    )