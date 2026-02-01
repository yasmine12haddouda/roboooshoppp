"""Context processors - cart count in all templates."""
from .services import CartService


def cart_context(request):
    """Add cart_count to every template."""
    cart_items, _ = CartService.get_cart_items(request)
    cart_count = sum(i["quantity"] for i in cart_items)
    return {"cart_count": cart_count}
