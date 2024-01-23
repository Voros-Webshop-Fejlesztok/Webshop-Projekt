from django.shortcuts import render
from .models import *

# Create your views here.

def store(request):
    products = Product.objects.all()
    
    product_name_query = request.GET.get('product_name')
    author_query = request.GET.get('author_name')

    if product_name_query != '' and product_name_query is not None:
        products = products.filter(pname__icontains=product_name_query)
    
    context = {'products':products}

    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)