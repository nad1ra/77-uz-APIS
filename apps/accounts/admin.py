from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Address, CustomUser


@admin.register(Address)
class AddressAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "lat", "long")
    search_fields = ("name",)
    list_filter = ("lat", "long")


class SellerChangeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        required=False,
        help_text="Yangi parol kiriting yoki bo‘sh qoldiring.",
    )

    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and password != self.instance.password:
            return make_password(password)
        return self.instance.password


@admin.register(CustomUser)
class SellerUserAdmin(TabbedTranslationAdmin):
    form = SellerChangeForm
    list_display = ("id", "full_name", "phone_number", "status", "is_active", "role")
    list_filter = ("status", "is_active", "role")
    search_fields = ("full_name", "phone_number")
    readonly_fields = ("last_login",)