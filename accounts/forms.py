"""Forms for auth - Single Responsibility: validation only."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role


class RegisterForm(UserCreationForm):
    """Registration form with role selection."""
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[(Role.BUYER, "Buyer"), (Role.SELLER, "Seller")],
        initial=Role.BUYER
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Simple login form."""
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
