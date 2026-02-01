"""Shop forms - product create/edit."""
from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """Form for product create/update - Single Responsibility."""

    class Meta:
        model = Product
        fields = ["name", "slug", "category", "description", "price", "stock", "image"]
