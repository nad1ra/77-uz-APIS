import random
import string
from common.validators import icon_extensions
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from store.models import Category


class Address(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super admin"
        ADMIN = "admin", "Admin"
        SELLER = "seller", "Sotuvchi"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    full_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    profile_photo = models.ImageField(
        upload_to="profiles/", null=True, blank=True, validators=[icon_extensions]
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.SELLER)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    plain_password = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.status == self.Status.APPROVED and not self.plain_password:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            self.set_password(password)
            self.plain_password = password
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number
