"""Role-based access decorators - Dependency Inversion."""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

from .models import Role


def role_required(*roles):
    """Decorator: require user to have one of the given roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("accounts:login")
            if request.user.role not in roles:
                messages.error(request, "You don't have permission.")
                return redirect("shop:home")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


admin_required = lambda f: role_required(Role.ADMIN)(f)
seller_required = lambda f: role_required(Role.SELLER, Role.ADMIN)(f)
