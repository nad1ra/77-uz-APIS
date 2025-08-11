from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Address, CustomUser


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "lat", "long")
    search_fields = ("name",)
    list_filter = ("lat", "long")


@admin.register(CustomUser)
class SellerUserAdmin(TabbedTranslationAdmin):
    list_display = (
        "id",
        "full_name",
        "phone_number",
        "status",
        "is_active",
        "role",
    )
    list_filter = ("status", "is_active", "role")
    search_fields = ("full_name", "phone_number")
    readonly_fields = ("last_login",)

    fieldsets = (
        (None, {
            "fields": (
                "phone_number",
                "full_name",
                "project_name",
                "profile_photo",
            )
        }),
        ("Tizim huquqlari", {
            "fields": (
                "role",
                "status",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Qo‘shimcha", {
            "fields": (
                "category",
                "address",
                "last_login",
            )
        }),
        ("Parol", {
            "fields": ("password",),
        }),
    )

    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
