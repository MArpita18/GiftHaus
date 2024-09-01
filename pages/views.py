from django.shortcuts import render
from Product.models import Product,Category

def index(request):
    categories = Category.objects.all().order_by('category')
    context = {
        'categories' : categories,
    }
    return render(request, 'pages/index.html', context)

def product_category(request, cid):
    products = Product.objects.filter(category=cid)
    categories = Category.objects.all().order_by('category')
    context = {
        'products' : products,
        'categories' : categories,
    }
    return render(request, 'Product/products.html',context)

def aboutus(request):
    return render(request, 'pages/aboutus.html')
