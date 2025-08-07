from django.core.exceptions import ValidationError


def icon_extensions(file):
    ext = file.name.split('.')[-1].lower()
    if ext not in ['png', 'jpg', 'jpeg', 'svg']:
        raise ValidationError("Ruxsat etilgan formatlar: png, jpg, jpeg, svg.")