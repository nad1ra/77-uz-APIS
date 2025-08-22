import uuid
from django.utils import timezone
from django.utils.text import slugify
from django.db import models


class BaseModel(models.Model):
    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Page(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            title_uz = getattr(self, 'title_uz', None)
            if title_uz:
                self.slug = slugify(title_uz)
            else:
                self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def str(self):
        return self.title


class Region(BaseModel):
    name = models.CharField(max_length=200, verbose_name="Region name")

    def __str__(self):
        return self.name


class District(BaseModel):
    region = models.ForeignKey(Region, related_name='districts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AppInfo(BaseModel):
    phone = models.CharField(max_length=20)
    support_email = models.EmailField()
    working_hours = models.CharField(max_length=200)
    app_version = models.CharField(max_length=20)
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"App Info ({self.app_version})"