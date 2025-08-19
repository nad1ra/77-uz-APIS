from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="child",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="category_icons/", null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Ad(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        PENDING = "pending", "Pending"
        REJECTED = "rejected", "Rejected"

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="ads")
    description = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ads")
    published_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    view_count = models.PositiveIntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_ads",
        blank=True
    )

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AdPhoto(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="ad_photos/")
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_main:
            AdPhoto.objects.filter(ad=self.ad, is_main=True).exclude(id=self.id).update(
                is_main=False
            )
        super().save(*args, **kwargs)

    def __str__(self):
        ad_name = self.ad.name_uz if self.ad_id else "No Ad"
        return f"{ad_name} - Photo"


class FavouriteProduct(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites",
        null=True,
        blank=True,
    )
    device_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="favourites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product",
                condition=models.Q(user__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["device_id", "product"],
                name="unique_device_product",
                condition=models.Q(device_id__isnull=False),
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        product_name = self.product.name if self.product_id else "No Product"
        user_or_device = self.user or self.device_id or "Anonymous"
        return f"{user_or_device} -> {product_name}"

