from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")

        user = self.model(phone_number=phone_number, **extra_fields)

        if password:
            user.set_password(password)
            user.plain_password = password
        else:
            user.set_unusable_password()
            user.plain_password = None

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("role", self.model.Role.SUPER_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("status", self.model.Status.APPROVED)

        if extra_fields.get("role") != self.model.Role.SUPER_ADMIN:
            raise ValueError("Superuser must have role=super_admin.")
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)

    def create_admin(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("role", self.model.Role.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("status", self.model.Status.APPROVED)

        if extra_fields.get("role") != self.model.Role.ADMIN:
            raise ValueError("Admin must have role=admin.")

        return self.create_user(phone_number, password, **extra_fields)

    def create_seller(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("role", self.model.Role.SELLER)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("status", self.model.Status.PENDING)

        if extra_fields.get("role") != self.model.Role.SELLER:
            raise ValueError("Seller must have role=seller.")

        return self.create_user(phone_number, password, **extra_fields)
