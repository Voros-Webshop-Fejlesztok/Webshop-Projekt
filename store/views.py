from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import *
from .forms import CreateUserForm, PostForm, UpdateProfileForm, DeletePostForm, SendMessage, DeleteMessageForm, CommentForm, DeleteCommentForm
from .utils import cookieCart, cartData, guestOrder
from django.conf import settings
from django.core.files import File
from django.core.files.images import ImageFile
import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if error == 'This password is too common.':
                        messages.success(request, 'Vegye már észre kolléga, ez a jelszó túl primitív!')
                    elif error == 'The password is too similar to the username.':
                        messages.success(request, 'Most komolyan? Ne hasonlítson már a jelszavad a felhasználónedhez!')
                    elif error == 'The password is too similar to the last name.' or error == 'The password is too similar to the first name.':
                        messages.success(request, 'Ne szórakozz már! Ne a saját neved takarja a jelszavad...')
                    elif error == 'A user with that username already exists.':
                        messages.success(request, 'Hoppá, valaki megelőzött. Ez a felhasználónév már foglalt.')
                    elif error == 'This password is too short. It must contain at least 8 characters.':
                        messages.success(request, 'Rövid szerszámmal szexelni sem lehet. Adjál már meg hosszabb jelszót!')
                    elif error == 'The two password fields didn’t match.':
                        messages.success(request, 'Most komolyan? Kétszer kellene ugyanazt a jelszót begépelned, de úgy látom neked már ez is nehezedre esik...')


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
            messages.success(request, 'Örülök, hogy betévedtél a Dáridó Shopba ' + username + ', de remélem, hogy nem a GPS hibázott!')
            return redirect('home')
        else:
            messages.info(request, 'Ha Póda Laci emlékszik arra, hogy 30 éve hogyan darált az AK-val, te is emlékezz a felhasználónév és jelszó kombinációdra')
            return redirect('login')

    return render(request, 'store/login.html', context)

def logoutUser(request):

    messages.success(request, 'Ahogy most kijelentkeztél, s majd bezárod a böngészőt, úgy nyiss ki egy üveg whiskeyt is, hisz minden fejezet lezárásánál egy új kezdődik az előző helyett.')

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
    digital = request.GET.get('digital')
    is_digital = False

    if digital == 'false':
        is_digital = False
    elif digital == 'true':
        is_digital = True
    
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

    if is_valid_param(is_digital):
        products = products.filter(digital=is_digital)
    
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
    order, created = Order.objects.get_or_create(customer = customer, status='not confirmed')

    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        current_product = orderItem.product
        current_product.stock -= 1
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        current_product = orderItem.product
        current_product.stock += 1
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    current_product.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status='not confirmed')
        
        order.pay=data['order_info']['payment']
        order.delivery=data['order_info']['delivery']
        order.total = data['order_info']['total']

    else:
        customer, order = guestOrder(request, data)
        order_items = OrderItem.objects.filter(order=order)
        products = Product.objects.filter(orderitem__in=order_items).distinct()

        for product in products:
            product.stock -= 1
            product.save()

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.status = 'confirmed'
    order.save()

    shipping = ''

    if order.shipping:
        shipping = ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    order_items = OrderItem.objects.filter(order=order)

    template = render_to_string('store/emails/processOrderEmail.html', {'name':customer.name, 'order':order, 'shipping':shipping, 'order_items':order_items})

    email = EmailMessage(
        'Köszönjük a rendelésed!',
        template,
        settings.EMAIL_HOST_USER,
        [customer.email],
    )

    email.content_subtype = "html"
    email.fail_silently=False
    email.send()

    return JsonResponse('Payment was complete', safe=False)



###########################################################

def forum(request):
    form = PostForm(request.POST or None)
    form2 = CommentForm(request.POST or None)
    if request.method == "POST":

        if 'delete_comment' in request.POST:
            delete_comment_form = DeleteCommentForm(request.POST)
            if delete_comment_form.is_valid():
                comment_id = delete_comment_form.cleaned_data['comment_id']
                del_comment = get_object_or_404(Comment, id=comment_id)
                del_comment.delete()
                messages.success(request, 'A komment sikeresen törlésre került')

        if 'create_post' in request.POST:
            if form.is_valid():
                post = form.save(commit=False)
                post.profile = request.user.customer
                post.save()
                messages.success(request, 'A posztod sikeresen létrejött')
                return redirect('forum')
            else:
                messages.info(request, 'A bejegyzés címe legfeljebb 50 karakter a tartalma pedig legfeljebb 1000 karakter lehet')

        if form2.is_valid():
            comy = form2.save(commit=False)
            comy.sender = request.user.customer
            post_value = request.POST.get('current_post')
            comy.post = Post(id=post_value)
            comy.save()
            messages.success(request, 'Sikeresen hozzászóltál a bejegyzéshez')
            return redirect('forum')

    posts = Post.objects.all().order_by("-created")

    search_text = request.GET.get('search_text')
    if is_valid_param(search_text):
        posts = posts.filter(Q(title__icontains=search_text)|Q(body__icontains=search_text)|Q(profile__user__username__icontains=search_text))

    profiles = Customer.objects.all()
    self_user = request.user.customer
    self_profile = Customer.objects.get(id=self_user.id)
    comments = Comment.objects.all().order_by("-created")
    comments_ids = []
    for comment in comments:
        if comment.post.id not in comments_ids:
            comments_ids.append(comment.post.id)

    context = {'profiles': profiles, 'self_profile': self_profile, 'posts': posts, 'form': form, 'form2': form2, 'comments':comments, 'comments_ids':comments_ids}

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

                current_profile = Customer.objects.get(id=profile2)

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

                    post_id = delete_post_form.cleaned_data['post_id']
                    post = get_object_or_404(Post, id=post_id)

                    post.delete()
                    messages.success(request, 'A poszt sikeresen törlésre került')

                return redirect(reverse('profile', kwargs={'pk': pk}))
                
            update_profile_form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=self_profile)
            if update_profile_form.is_valid():
                update_profile_form.save()
                return redirect(reverse('profile', kwargs={'pk': pk}))

    context = {'profile':profile, 'self_profile':self_profile,  'orders':orders, 'order_items':order_items, 'products':products, 'posts':posts, 'update_profile_form':update_profile_form, 'delete_post_form': delete_post_form,}

    return render(request, 'store/profile.html', context)

def message(request):
    delete_message_form = DeletePostForm
    friend_query = request.GET.get('friend_name')

    form = SendMessage(request.POST or None)
    self_user = request.user.customer
    self_profile = Customer.objects.get(id=self_user.id)
    self_friends = self_profile.friends
    self_messages = Message.objects.all().filter(Q(receiver=self_profile) | Q(sender=self_profile)).order_by("sent_date")
    current_friend = self_profile.last_friend

    if is_valid_param(friend_query):
        self_profile_followers = self_profile.followers.filter(name__icontains=friend_query)
        self_profile_follows = self_profile.follows.filter(name__icontains=friend_query)
        self_friends = self_profile_followers.intersection(self_profile_follows)

    last_messages_with_friends = []
    for friend in self_profile.friends:
        last_message_with_friend = self_messages.filter(Q(sender=self_profile, receiver=friend) | Q(sender=friend, receiver=self_profile)).last()
        last_messages_with_friends.append((friend, last_message_with_friend))

    if request.method == 'POST':
        current_friend = request.POST.get('friend_name')
        if current_friend:
            current_friend = Customer.objects.get(id=current_friend)
            self_profile.last_friend = current_friend
            self_profile.save()

        if form.is_valid():
            self_message = form.save(commit=False)
            self_message.sender = self_profile
            self_message.receiver = self_profile.last_friend
            self_message.content = form['content'].value()
            self_message.save()
            return redirect('message')
        
        if 'delete_message' in request.POST:
            delete_message_form = DeleteMessageForm(request.POST)
            if delete_message_form.is_valid():
                message_id = delete_message_form.cleaned_data['message_id']
                message = get_object_or_404(Message, id=message_id)
                message.delete()
                
                return redirect('message')


    context = {'self_profile': self_profile, 'current_friend': current_friend, 'self_messages': self_messages,
               'form': form, 'last_messages_with_friends': last_messages_with_friends,'self_friends':self_friends, 'delete_message_form':delete_message_form}

    return render(request, 'store/message.html', context)

def owner(request):
    orders = Order.objects.all()
    order_id = request.GET.get('order_id')
    order_items = OrderItem.objects.filter(order__in=orders)
    products = Product.objects.filter(orderitem__in=order_items).distinct()

    if is_valid_param(order_id):
        orders = orders.filter(id = order_id)

    if request.method == "POST":
        for order in orders:
            key = f'status;{order.id}'
            if key in request.POST:
                current_order = Order.objects.get(id=order.id)
                data = request.POST[f'status;{order.id}']
                print(data)
                if data == 'completed':
                    current_order.delete()
                else:
                    current_order.status = data
                    current_order.save()

        return redirect('owner')


    context = {'orders':orders, 'order_items':order_items, 'products':products}

    return render(request, 'store/owner.html', context)

def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    self_user = request.user.customer
    self_profile = Customer.objects.get(id=self_user.id)

    if post.likes.filter(id=self_profile.id):
        post.likes.remove(self_profile)
    else:
        post.likes.add(self_profile)

    return redirect('forum')
