from django.core.exceptions import ValidationError

def icon_extensions(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']
    if not any([file.name.endswith(ext) for ext in valid_extensions]):
        raise ValidationError('Fayl formati ruxsat etilmagan. Faqat JPG, PNG yoki SVG.')
