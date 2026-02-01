"""Shop forms - product, checkout."""
from django import forms
from .models import Product, Category
from .constants import WILAYAS, PAYMENT_METHODS


class ProductForm(forms.ModelForm):
    """Form for product create/update with image upload."""

    class Meta:
        model = Product
        fields = ["name", "slug", "category", "description", "price", "stock", "image"]


class CheckoutForm(forms.Form):
    """Checkout form - buyer contact info, wilaya, payment."""
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=30)
    wilaya = forms.ChoiceField(choices=[("", "Select Wilaya")] + list(WILAYAS))
    address = forms.CharField(max_length=255, widget=forms.Textarea(attrs={"rows": 2}))
    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS)
