from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Category, Ad, AdPhoto, FavouriteProduct, MySearch, SearchCount


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "parent", "type")
    search_fields = ("name", "type")
    list_filter = ("parent",)


class AdPhotoInline(admin.TabularInline):
    model = AdPhoto
    extra = 1
    fields = ("image", "is_main", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Ad)
class AdAdmin(TabbedTranslationAdmin):  # ✅
    list_display = ("id", "name", "category", "seller", "price", "status", "published_at", "view_count")
    search_fields = ("name", "description")
    list_filter = ("category", "status", "published_at")
    inlines = [AdPhotoInline]
    readonly_fields = ("published_at", "updated_time", "view_count")
    prepopulated_fields = {"name": ("name",)}


@admin.register(AdPhoto)
class AdPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "ad", "is_main", "created_at")
    list_filter = ("is_main", "ad")
    readonly_fields = ("created_at",)


@admin.register(FavouriteProduct)
class FavouriteProductAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "device_id", "product", "created_at")
    list_filter = ("user", "device_id", "product")
    readonly_fields = ("created_at",)


@admin.register(MySearch)
class MySearchAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "search_query", "category", "region", "price_min", "price_max", "created_at")
    list_filter = ("category", "region", "created_at")
    search_fields = ("search_query", "user__username", "user__phone_number")
    readonly_fields = ("created_at",)


@admin.register(SearchCount)
class SearchCountAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "search_count", "updated_at")
    list_filter = ("category",)
    readonly_fields = ("updated_at",)
