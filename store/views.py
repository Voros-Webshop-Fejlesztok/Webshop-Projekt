from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import CreateUserForm


# Create your views here.

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            user_name = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            name = first_name + ' ' + last_name

            user = User.objects.get(username = user_name)
            customer = Customer(user=user, email=email, name=name)
            
            customer.save()

            messages.success(request, 'Sikeresen létrehoztuk a ' + user_name + ' nevű fiókját')

            return redirect('login')

    context = {'form':form}
    return render(request, 'store/register.html', context)

def loginPage(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Helytelen felhasználónév vagy jelszó')
            return redirect('login')

    return render(request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


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
        products = products.filter(category__name__icontains=product_name_query)

        if len(products) == 0:
            products = Product.objects.all()
            products = products.filter(brand__name__icontains=product_name_query)

            if len(products) == 0:
                products = Product.objects.all()
                products = products.filter(pname__icontains=product_name_query)

                if len(products) == 0:
                    products = Product.objects.all()
                    products = products.filter(description__icontains=product_name_query)
            

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
    
    context = {'products':products,'categories':categories,'categories2':categories2,'brands':brands, 'shipping':False}

    return render(request, 'store/store.html', context)

######################################################################################################

def home(request):
    context = {}
    return render(request, 'store/home.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print(cart)
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

        for i in cart:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'pname':product.pname,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
    
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #ezzel csinál üres kosarakat az új és nem bejelentkezett felhasználóknak
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    user = request.user

    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity + -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],  
            )

    else:
        print('Nincs bejelentkezett felhasználó')

    return JsonResponse('Payment was complete', safe=False)