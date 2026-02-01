"""Shop views - Controller (MVC), uses services for business logic."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from accounts.decorators import seller_required, admin_required
from .models import Product, Category
from .forms import ProductForm


def home_view(request):
    """Home page - list products and categories."""
    products = Product.objects.filter(stock__gt=0).select_related("category", "seller")
    categories = Category.objects.all()
    q = request.GET.get("q", "")
    cat = request.GET.get("category", "")
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if cat:
        products = products.filter(category__slug=cat)
    context = {"products": products, "categories": categories}
    return render(request, "shop/home.html", context)


def product_detail_view(request, slug):
    """Product detail page."""
    product = get_object_or_404(Product, slug=slug)
    return render(request, "shop/product_detail.html", {"product": product})


@login_required
@seller_required
@require_http_methods(["GET", "POST"])
def product_create_view(request):
    """Create product - seller only."""
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect("shop:product_detail", slug=product.slug)
    else:
        form = ProductForm()
    return render(request, "shop/product_form.html", {"form": form, "title": "Add Product"})


@login_required
@seller_required
@require_http_methods(["GET", "POST"])
def product_edit_view(request, slug):
    """Edit product - seller only (own products)."""
    product = get_object_or_404(Product, slug=slug)
    if product.seller != request.user and not request.user.is_admin_role():
        return redirect("shop:home")
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("shop:product_detail", slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, "shop/product_form.html", {"form": form, "title": "Edit Product"})


@login_required
@seller_required
@require_http_methods(["POST"])
def product_delete_view(request, slug):
    """Delete product - seller only."""
    product = get_object_or_404(Product, slug=slug)
    if product.seller != request.user and not request.user.is_admin_role():
        return redirect("shop:home")
    product.delete()
    return redirect("shop:home")
