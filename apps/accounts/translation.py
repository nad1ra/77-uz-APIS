from modeltranslation.translator import TranslationOptions, register

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
