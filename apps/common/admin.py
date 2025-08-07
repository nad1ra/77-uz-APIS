from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Page, Region, District, AppInfo


@admin.register(Page)
class PageAdmin(TabbedTranslationAdmin):
    list_display = ("id", "slug", "title")
    search_fields = ("slug", "title")
    ordering = ("id",)
    list_per_page = 25


@admin.register(Region)
class RegionAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("id",)
    list_per_page = 25


@admin.register(District)
class DistrictAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "region")
    list_filter = ("region",)
    search_fields = ("name",)
    ordering = ("id",)
    list_per_page = 25


@admin.register(AppInfo)
class SettingAdmin(TabbedTranslationAdmin):
    list_display = ("phone", "support_email", "app_version", "maintenance_mode")
    search_fields = ("phone", "support_email", "app_version")
    list_filter = ("maintenance_mode",)
    list_per_page = 25
