"""AuthService - Registration, authentication, seller checks, profile management."""
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthService:
    """User authentication and profile management."""

    @staticmethod
    def register_user(form, request=None):
        """Register new user and optionally log in."""
        user = form.save(commit=False)
        user.email = form.cleaned_data.get("email", user.email)
        user.role = form.cleaned_data.get("role", user.role)
        user.save()
        if request and user:
            login(request, user)
        return user

    @staticmethod
    def authenticate_user(request, username, password):
        """Authenticate user by username or email."""
        user = authenticate(request, username=username, password=password)
        if not user:
            user = User.objects.filter(email=username).first()
            if user and user.check_password(password):
                return user
        return user

    @staticmethod
    def is_seller(user):
        """Check if user is seller or admin."""
        return user and (user.role == "seller" or user.role == "admin")

    @staticmethod
    def get_or_create_seller_profile(user):
        """Get or create seller profile for user."""
        from .models import Seller
        profile, _ = Seller.objects.get_or_create(user=user)
        return profile

    @staticmethod
    def update_seller_profile(user, phone, address):
        """Update seller profile."""
        profile = AuthService.get_or_create_seller_profile(user)
        profile.phone = phone
        profile.address = address
        profile.save()
        return profile
