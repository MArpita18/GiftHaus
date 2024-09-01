from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from Product.models import Product,Category,Order
from user.models import Address
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date, timedelta

def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.all().order_by('category')
    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, 'Product/products.html', context)

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    quantity=1
    cart_items = request.session.get('cart_items')
    if cart_items and str(id) in cart_items:
        quantity = cart_items[str(id)]
    context = {
        "product": product,
        "quantity": quantity,
    }
    return render(request, 'Product/product_details.html', context)
    
def product_category(request, cid):
    products = Product.objects.filter(category=cid)
    categories = Category.objects.all().order_by('category')
    context = {
        'products' : products,
        'categories' : categories,
    }
    return render(request, 'Product/products.html',context)


def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        cart_items = {}
        if request.session.get("cart_items"):
            cart_items = (request.session.get("cart_items"))
        cart_items[product_id] = quantity 
        request.session["cart_items"] = cart_items
        print(request.session.get("cart_items"))
    return redirect("cart")

def cart(request):
    cart_details, total_price = get_cart_details(request)
    context = {
        "products" : cart_details,
        "total_price" : total_price
    }
    return render(request, "Product/cart.html", context)

def remove_from_cart(request,id):
    cart_items = request.session.get("cart_items")
    del cart_items[str(id)]
    request.session["cart_items"] = cart_items
    return redirect("cart")

def check_out(request):
    addresses = Address.objects.filter(user=request.user)
    cart_details, total_price = get_cart_details(request)
    context ={
        "addresses": addresses,
        "products": cart_details,
        "total_price": total_price
    }
    return render(request, "Product/check_out.html", context)

def place_order(request):
    if request.method == "POST":
        user = request.user
        address = request.POST.get('address')
        address = Address.objects.get(id=address)
        payment_mode = request.POST.get('payment_mode')
        cart_details, total_price = get_cart_details(request)
        orders = []
        for product in cart_details:
            order = Order(
                Product = Product.objects.get(id=product['id']),
                user = user,
                address = address,
                quantity = product['quantity'],
                price = product['price'],
                payment_method = payment_mode
            )
            orders.append(order)
        Order.objects.bulk_create(orders)
        request.session['cart_items'] = {}
        return redirect('all_products')

def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'orders': orders
    }
    return render(request, 'Product/orders.html', context) 

def cancel_order(request, order_id):
    order = Order.objects.get(pk=order_id)

    order.status = 'Canceled'
    order.save()
    
def get_cart_details(request):
    total_price = 0
    cart_details = []
    if not request.session.get("cart_items"):
        return cart_details, total_price
    
    cart_items = request.session.get("cart_items")
    products = Product.objects.filter(id__in=list(cart_items.keys()))
    
    for product in products:
        quantity = int(cart_items[str(product.id)])
        price = quantity * product.price
        total_price += price
        cart_details.append({
            "id": product.id,
            "name": product.name,
            "quantity": quantity,
            "price": price,
            "image": product.image
        })
    return cart_details, total_price
    
