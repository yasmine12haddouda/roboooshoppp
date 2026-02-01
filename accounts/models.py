"""User model with role-based access (Admin, Seller, Buyer)."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    """User roles - Single Responsibility: define roles."""
    ADMIN = "admin", "Admin"
    SELLER = "seller", "Seller"
    BUYER = "buyer", "Buyer"


class User(AbstractUser):
    """Custom User with role - follows Interface Segregation."""
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.BUYER
    )
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def is_admin_role(self):
        return self.role == Role.ADMIN

    def is_seller_role(self):
        return self.role == Role.SELLER

    def is_buyer_role(self):
        return self.role == Role.BUYER


class Seller(models.Model):
    """Seller profile - OneToOne with User, phone, address."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seller_profile"
    )
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
