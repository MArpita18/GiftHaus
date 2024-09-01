from django.urls import path
from Product.views import all_products,product_details, product_category, add_to_cart,cart,remove_from_cart,check_out,place_order,orders,cancel_order

urlpatterns = [
    path('', all_products, name = "all_products"),
    path('<int:id>/', product_details, name = "product_details"),
    path("category/<int:cid>", product_category, name="product_category"),
    path("add_to_cart", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("remove_from_cart/<int:id>/", remove_from_cart, name="remove_from_cart"),
    path("check_out/", check_out, name="check_out"),
    path("place_order/", place_order, name="place_order"),
    path("orders/", orders, name="orders"),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
]

