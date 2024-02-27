from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import CreateUserForm, PostForm, UpdateProfileForm, DeletePostForm
from django.db.models import Q

from .utils import cookieCart, cartData, guestOrder

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
            customer = Customer(user=user, email=email, name=name, phone_number='')
            
            customer.save()

            messages.success(request, 'Sikeresen létrehoztuk a ' + user_name + ' nevű felhasználói fiókját')

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
            messages.success(request, 'Sikeresen bejelentkezett ' + username + ' felhasználó')
            return redirect('home')
        else:
            messages.info(request, 'Helytelen felhasználónév vagy jelszó')
            return redirect('login')

    return render(request, 'store/login.html', context)

def logoutUser(request):

    messages.success(request, 'Sikeresen kijelentkezett')

    logout(request)

    return redirect('login')


def is_valid_param(param):
    return param != '' and param is not None

def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    product_name_query = request.GET.get('product_name')
    rating_min = request.GET.get('rating_min')
    rating_max = request.GET.get('rating_max')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    
    

    if is_valid_param(product_name_query):
        products = products.filter(Q(pname__icontains=product_name_query)|  Q(brand__name__icontains=product_name_query)|  Q(category__name__icontains=product_name_query)|  Q(pname__icontains=product_name_query)|  Q(description__icontains=product_name_query))

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
        
    if is_valid_param(brand) and brand != '':
        products = products.filter(brand__name=brand)
    
    context = {'products':products,'categories':categories,'brands':brands, 'shipping':False}

    return render(request, 'store/store.html', context)

######################################################################################################

def home(request):
    context = {}

    return render(request, 'store/home.html', context)

def cart(request):
    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

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
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping:
        ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Payment was complete', safe=False)



###########################################################

def forum(request):
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.profile = request.user.customer
            post.save()
            messages.success(request, 'A posztod sikeresen létrejött')
            return redirect('forum')
        else:
            messages.info(request, 'A bejegyzés címe legfeljebb 50 karakter a tartalma pedig legfeljebb 1000 karakter lehet')

    posts = Post.objects.all().order_by("-created")

    profiles = Customer.objects.all()

    self_user = request.user.customer
    self_profile = Customer.objects.get(id=self_user.id)

    context = {'profiles': profiles, 'self_profile': self_profile, 'posts': posts, 'form': form}

    return render(request, 'store/forum.html', context)

def profile(request, pk):
    
    if request.user.is_authenticated:
        delete_post_form = DeletePostForm()
        profile = Customer.objects.get(user_id=pk)

        posts = Post.objects.all().order_by("-created")
        posts = posts.filter(profile=profile)
        
        self_user = request.user.customer
        self_profile = Customer.objects.get(id=self_user.id)


        orders = Order.objects.all().filter(customer_id=profile.id)
        order_items = OrderItem.objects.filter(order__in=orders)
        products = Product.objects.filter(orderitem__in=order_items).distinct()

        update_profile_form = UpdateProfileForm(instance=self_profile)

        if request.method == "POST":

            if 'follow' in request.POST:
                data = request.POST['follow'].split(';')
                action = data[0]
                profile2 = data[1]

                current_profile = Customer.objects.get(name=profile2)

                if action == 'unfollow':
                    self_profile.follows.remove(current_profile)
                    current_profile.followers.remove(self_profile)
                elif action == 'follow':
                    self_profile.follows.add(current_profile)
                    current_profile.followers.add(self_profile)
                        
                self_profile.save()
                current_profile.save()

            if 'delete_post' in request.POST:
                delete_post_form = DeletePostForm(request.POST)
                if delete_post_form.is_valid():
                    print('jaja')
                    post_id = delete_post_form.cleaned_data['post_id']
                    post = get_object_or_404(Post, id=post_id)

                    post.delete()
                    messages.success(request, 'A poszt sikeresen törlésre került')

                return redirect(reverse('profile', kwargs={'pk': pk}))
                
            update_profile_form = UpdateProfileForm(request.POST, instance=self_profile)
            if update_profile_form.is_valid():
                update_profile_form.save()
                return redirect(reverse('profile', kwargs={'pk': pk}))

    context = {'profile':profile, 'self_profile':self_profile,  'orders':orders, 'order_items':order_items, 'products':products, 'posts':posts, 'update_profile_form':update_profile_form, 'delete_post_form': delete_post_form,}

    return render(request, 'store/profile.html', context)

def messages(request):
    self_user = request.user.customer
    self_profile = Customer.objects.get(id=self_user.id)

    current_friend = Customer.objects.get(name='Csete Ádám')

    self_messages = Message.objects.all().filter(Q(receiver=self_profile)|  Q(sender=self_profile)).order_by("sent_date")

    context = {'self_profile':self_profile,'current_friend':current_friend, 'self_messages':self_messages}

    return render(request, 'store/messages.html', context)
