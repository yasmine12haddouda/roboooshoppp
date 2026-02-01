"""Shop views - Controller (MVC), uses services for business logic."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.contrib import messages

from accounts.decorators import seller_required
from .models import Product, Category, Order
from .forms import ProductForm, CheckoutForm
from .services import ProductService, CartService, OrderService


def home_view(request):
    """Home page - products grouped by category."""
    categories = Category.objects.all().order_by("name")
    q = request.GET.get("q", "")
    cat = request.GET.get("category", "")
    view_all = request.GET.get("view_all") == "1"
    products_qs = Product.objects.filter(stock__gt=0).select_related("category", "seller").order_by("category__name", "name")
    if q:
        products_qs = products_qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if cat:
        products_qs = products_qs.filter(category__slug=cat)
    # Group products by category for main page
    products_by_category = {}
    for p in products_qs:
        key = (p.category.id, p.category.name, p.category.slug)
        if key not in products_by_category:
            products_by_category[key] = []
        products_by_category[key].append(p)
    # Limit to 6 per category unless view_all or single category filter
    limit = 6 if not (view_all or cat) else 999
    for key in products_by_category:
        products_by_category[key] = products_by_category[key][:limit]
    context = {"products_by_category": products_by_category, "categories": categories, "q": q, "cat": cat}
    return render(request, "shop/home.html", context)


def product_detail_view(request, slug):
    """Product detail page."""
    product = get_object_or_404(Product, slug=slug)
    cart_items, _ = CartService.get_cart_items(request)
    cart_count = sum(i["quantity"] for i in cart_items)
    return render(request, "shop/product_detail.html", {"product": product, "cart_count": cart_count})


@require_http_methods(["POST"])
def cart_add_view(request, product_id):
    """Add item to cart."""
    quantity = int(request.POST.get("quantity", 1))
    success, err = CartService.add_item(request, product_id, quantity)
    if success:
        messages.success(request, "Added to cart.")
    else:
        messages.error(request, err or "Could not add to cart.")
    return redirect(request.META.get("HTTP_REFERER", "shop:home"))


@require_http_methods(["POST"])
def cart_remove_view(request, product_id):
    """Remove item from cart."""
    CartService.remove_item(request, product_id)
    messages.success(request, "Removed from cart.")
    return redirect("shop:cart")


@require_http_methods(["POST"])
def cart_update_view(request, product_id):
    """Update cart item quantity."""
    quantity = int(request.POST.get("quantity", 1))
    success, err = CartService.update_quantity(request, product_id, quantity)
    if not success:
        messages.error(request, err or "Invalid quantity.")
    return redirect("shop:cart")


def cart_view(request):
    """View cart with totals."""
    cart_items, total = CartService.get_cart_items(request)
    cart_count = sum(i["quantity"] for i in cart_items)
    return render(request, "shop/cart.html", {"cart_items": cart_items, "total": total, "cart_count": cart_count})


@login_required
@require_http_methods(["GET", "POST"])
def checkout_view(request):
    """Checkout - collect buyer info, create order."""
    cart_items, total = CartService.get_cart_items(request)
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect("shop:home")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        order, err = OrderService.process_checkout(request, form)
        if order:
            return redirect("shop:order_success", order_id=order.id)
        messages.error(request, err or "Checkout failed.")
    else:
        form = CheckoutForm(initial={
            "first_name": request.user.first_name or "",
            "last_name": request.user.last_name or "",
            "phone": request.user.phone or "",
        })
    cart_count = sum(i["quantity"] for i in cart_items)
    return render(request, "shop/checkout.html", {
        "form": form, "cart_items": cart_items, "total": total, "cart_count": cart_count
    })


@login_required
def order_success_view(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "shop/order_success.html", {"order": order})


@login_required
@seller_required
def seller_dashboard_view(request):
    """Seller dashboard - products, recent orders."""
    from .models import OrderItem
    products = Product.objects.filter(seller=request.user).select_related("category")
    order_items = OrderItem.objects.filter(seller=request.user).select_related(
        "order", "product"
    ).order_by("-order__created_at")[:50]
    orders_by_id = {}
    for oi in order_items:
        oid = oi.order_id
        if oid not in orders_by_id:
            orders_by_id[oid] = {"order": oi.order, "items": []}
        orders_by_id[oid]["items"].append(oi)
    recent_orders = list(orders_by_id.values())
    return render(request, "shop/seller_dashboard.html", {
        "products": products, "recent_orders": recent_orders
    })


@login_required
@seller_required
@require_http_methods(["GET", "POST"])
def product_create_view(request):
    """Create product - seller only, with image upload."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = ProductService.create_product(form, request.user)
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
        form = ProductForm(request.POST, request.FILES, instance=product)
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
