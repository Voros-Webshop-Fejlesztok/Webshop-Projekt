from django.shortcuts import render
from .models import *

# Create your views here.

def is_valid_param(param):
    return param != '' and param is not None

def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    categories2 = Category2.objects.all()
    brands = Brand.objects.all()
    
    product_name_query = request.GET.get('product_name')
    rating_min = request.GET.get('rating_min')
    rating_max = request.GET.get('rating_max')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category = request.GET.get('category')
    category2 = request.GET.get('category2')
    brand = request.GET.get('brand')
    

    if is_valid_param(product_name_query):
        products = products.filter(pname__icontains=product_name_query)


    if is_valid_param(rating_min):
        products = products.filter(rating__gte=rating_min)

    if is_valid_param(rating_max):
        products = products.filter(rating__lt=rating_max)

    if is_valid_param(price_min):
        products = products.filter(price__gte=price_min)

    if is_valid_param(price_max):
        products = products.filter(price__lt=price_max)

    if is_valid_param(category) and category != '':
        products = products.filter(category__name=category)

    if is_valid_param(category2) and category2 != '':
        products = products.filter(category2__name=category2)
        
    if is_valid_param(brand) and brand != '':
        products = products.filter(brand__name=brand)
    
    context = {'products':products,'categories':categories,'categories2':categories2,'brands':brands}

    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)