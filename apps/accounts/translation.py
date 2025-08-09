from modeltranslation.translator import TranslationOptions, register
from store.models import Category

from .models import Address, CustomUser


@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    fields = (
        "full_name",
        "project_name",
    )


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)