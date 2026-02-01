"""Auth views - Controller layer (MVC)."""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .forms import LoginForm, RegisterForm, SellerProfileForm
from .services import AuthService
from .decorators import seller_required


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Handle user registration with role selection."""
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = AuthService.register_user(form, request)
            if user.role == "seller":
                AuthService.get_or_create_seller_profile(user)
            return redirect("shop:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle login - email or username authentication."""
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = AuthService.authenticate_user(
                request,
                form.cleaned_data["username"],
                form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("shop:home")
            form.add_error(None, "Invalid username/email or password")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
@require_http_methods(["POST", "GET"])
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect("shop:home")


@login_required
@seller_required
@require_http_methods(["GET", "POST"])
def seller_profile_view(request):
    """Seller profile management - phone, address."""
    profile = AuthService.get_or_create_seller_profile(request.user)
    if request.method == "POST":
        form = SellerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:seller_profile")
    else:
        form = SellerProfileForm(instance=profile)
    return render(request, "accounts/seller_profile.html", {"form": form})
