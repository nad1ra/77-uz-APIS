from modeltranslation.translator import register, TranslationOptions
from .models import Category, Ad


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Ad)
class AdTranslationOptions(TranslationOptions):
    fields = ("name", "description")
