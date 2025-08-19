from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Category, Ad, AdPhoto, FavouriteProduct


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "parent")
    search_fields = ("name",)


class AdPhotoInline(admin.TabularInline):
    model = AdPhoto
    extra = 1


@admin.register(Ad)
class AdAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "category", "price", "status", "seller")
    list_filter = ("status", "category")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AdPhotoInline]


@admin.register(FavouriteProduct)
class FavouriteProductAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "device_id", "product", "created_at")
    search_fields = ("user__username", "device_id")
