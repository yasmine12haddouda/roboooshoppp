"""Shop URL routes."""
from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("product/add/", views.product_create_view, name="product_create"),
    path("product/<slug:slug>/edit/", views.product_edit_view, name="product_edit"),
    path("product/<slug:slug>/", views.product_detail_view, name="product_detail"),
    path("product/<slug:slug>/delete/", views.product_delete_view, name="product_delete"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add_view, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove_view, name="cart_remove"),
    path("cart/update/<int:product_id>/", views.cart_update_view, name="cart_update"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("order/<int:order_id>/success/", views.order_success_view, name="order_success"),
    path("seller/dashboard/", views.seller_dashboard_view, name="seller_dashboard"),
]
