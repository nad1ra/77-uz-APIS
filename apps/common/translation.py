from modeltranslation.translator import register, TranslationOptions
from .models import Page, Region, District, AppInfo


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(AppInfo)
class AppInfoTranslationOptions(TranslationOptions):
    fields = ('working_hours',)
