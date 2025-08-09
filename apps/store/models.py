from django.db import models
from common.models import BaseModel
from common.validators import icon_extensions


class Category(BaseModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="child",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    icon = models.FileField(
        upload_to='categories/', validators=[icon_extensions], null=True, blank=True
    )

    def __str__(self):
        return getattr(self, 'name', 'Category')
