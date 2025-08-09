from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "phone_number",
        "full_name",
        "project_name",
        "status",
        "show_plain_password",
    )
    list_filter = ("status", "category")
    search_fields = ("phone_number", "full_name", "project_name")
    ordering = ("-id",)

    fieldsets = (
        (None, {"fields": ("phone_number", "email", "plain_password")}),
        (
            "Personal Info",
            {"fields": ("full_name", "project_name", "category", "address")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_seller",
                    "is_staff",
                    "is_superuser",
                    "status",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "email", "password1", "password2", "status"),
            },
        ),
    )

    def show_plain_password(self, obj):
        if obj.status == "approved":
            return obj.plain_password or "Parol yo‘q"
        return "Yashirilgan"

    show_plain_password.short_description = "Parol"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("name", "lat", "long")
