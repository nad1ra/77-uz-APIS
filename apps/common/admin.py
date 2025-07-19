from django.contrib import admin
from .models import Page, Region, District, AppInfo


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fields = (
        'title_uz', 'title_ru',
        'content_uz', 'content_ru',
        'slug',
    )

    list_display = ('title_uz', 'slug')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    fields = ('name_uz', 'name_ru')
    list_display = ('name_uz', 'name_ru')
    search_fields = ('name_uz', 'name_ru')



@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    fields = ('name_uz', 'name_ru', 'region')
    list_display = ('name_uz', 'name_ru', 'get_region_name')
    list_filter = ('region',)
    search_fields = ('name_uz', 'name_ru')

    def get_region_name(self, obj):
        return obj.region.name_uz
    get_region_name.short_description = 'Region (Uz)'


@admin.register(AppInfo)
class AppInfoAdmin(admin.ModelAdmin):
    list_display = (
        'phone',
        'support_email',
        'app_version',
        'maintenance_mode'
    )
    list_filter = ('maintenance_mode',)
    search_fields = ('phone', 'support_email', 'app_version')

    fields = (
        'phone',
        'support_email',
        'working_hours_uz',
        'working_hours_ru',
        'app_version',
        'maintenance_mode',
    )

    exclude = ('working_hours',)

