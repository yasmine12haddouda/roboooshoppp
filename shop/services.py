"""Shop services - ProductService, CartService, OrderService (Business Logic)."""
from decimal import Decimal
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ProductService:
    """Product creation, retrieval, validation."""

    @staticmethod
    def create_product(form, seller):
        """Create product with seller."""
        from .models import Product
        product = form.save(commit=False)
        product.seller = seller
        product.save()
        return product

    @staticmethod
    def validate_stock(product, quantity):
        """Check product availability."""
        return product and product.stock >= quantity and quantity > 0

    @staticmethod
    def is_available(product):
        """Check if product is in stock."""
        return product and product.stock > 0


class CartService:
    """Session-based cart - add/remove, totals, stock validation."""

    CART_KEY = "cart"

    @classmethod
    def get_cart(cls, request):
        """Get cart from session."""
        cart = request.session.get(cls.CART_KEY, {})
        return dict(cart)

    @classmethod
    def add_item(cls, request, product_id, quantity=1):
        """Add item to cart with stock validation."""
        from .models import Product
        product = Product.objects.filter(id=product_id).first()
        if not ProductService.validate_stock(product, quantity):
            return False, "Invalid stock"
        cart = cls.get_cart(request)
        key = str(product_id)
        current = cart.get(key, 0)
        new_qty = current + quantity
        if not ProductService.validate_stock(product, new_qty):
            return False, "Not enough stock"
        cart[key] = new_qty
        request.session[cls.CART_KEY] = cart
        request.session.modified = True
        return True, None

    @classmethod
    def remove_item(cls, request, product_id):
        """Remove item from cart."""
        cart = cls.get_cart(request)
        cart.pop(str(product_id), None)
        request.session[cls.CART_KEY] = cart
        request.session.modified = True

    @classmethod
    def update_quantity(cls, request, product_id, quantity):
        """Update item quantity with stock validation."""
        from .models import Product
        product = Product.objects.filter(id=product_id).first()
        if not ProductService.validate_stock(product, quantity):
            return False, "Invalid stock"
        cart = cls.get_cart(request)
        cart[str(product_id)] = quantity
        request.session[cls.CART_KEY] = cart
        request.session.modified = True
        return True, None

    @classmethod
    def get_cart_items(cls, request):
        """Get cart with product details and totals."""
        from .models import Product
        cart = cls.get_cart(request)
        items = []
        total = Decimal("0")
        for pid, qty in cart.items():
            product = Product.objects.filter(id=pid).select_related("seller", "category").first()
            if product and ProductService.validate_stock(product, qty):
                subtotal = product.price * qty
                items.append({"product": product, "quantity": qty, "subtotal": subtotal})
                total += subtotal
        return items, total

    @classmethod
    def clear_cart(cls, request):
        """Clear cart after checkout."""
        request.session[cls.CART_KEY] = {}
        request.session.modified = True


class OrderService:
    """Checkout validation, order processing, stock reduction, payment creation."""

    @staticmethod
    def process_checkout(request, form):
        """Validate cart, create order, reduce stock, create payment."""
        from .models import Order, OrderItem, Payment
        cart_items, total = CartService.get_cart_items(request)
        if not cart_items:
            return None, "Cart is empty"
        if not form.is_valid():
            return None, "Invalid form"
        data = form.cleaned_data
        order = Order.objects.create(
            user=request.user,
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            wilaya=data["wilaya"],
            address=data["address"],
            payment_method=data["payment_method"],
            total_price=total,
        )
        for item in cart_items:
            product = item["product"]
            qty = item["quantity"]
            price = product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                seller=product.seller,
                quantity=qty,
                price=price,
            )
            product.stock -= qty
            product.save()
        Payment.objects.create(
            user=request.user,
            order=order,
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            wilaya=data["wilaya"],
            address=data["address"],
            amount=total,
            payment_method=data["payment_method"],
        )
        CartService.clear_cart(request)
        return order, None
