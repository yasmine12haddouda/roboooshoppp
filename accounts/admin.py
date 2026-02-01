"""Admin config for accounts."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Seller


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role",)
    fieldsets = BaseUserAdmin.fieldsets + (("Role", {"fields": ("role", "phone", "address")}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (("Role", {"fields": ("role", "email")}),)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "address")
