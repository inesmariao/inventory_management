from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    Handles user and superuser creation using email as the unique identifier.
    """
    def create_user(self, email, password=None, role='external', **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with two roles:
    - Administrator: full access to create/edit/delete companies and products
    - External: read-only access to companies
    """

    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('external', 'External'),
    )

    email = models.EmailField(
        unique=True,
        help_text="Required. A valid email address used as the unique identifier for authentication."
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='external',
        help_text="User role: 'admin' has full permissions, 'external' has read-only access."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active."
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into the Django admin site."
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the user was deactivated (soft deleted)."
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
