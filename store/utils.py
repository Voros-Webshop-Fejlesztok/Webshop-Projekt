import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
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
        except:
            pass
    return {'cartItems':cartItems, 'items':items, 'order':order}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status='not confirmed')
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    return {'cartItems':cartItems, 'items':items, 'order':order}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']
    phonenumber = data['form']['phonenumber']
    pay = data['order_info']['payment']
    delivery = data['order_info']['delivery']
    total = data['order_info']['total']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
        phone_number=phonenumber,
        name=name
    )

    customer.save()

    order = Order.objects.create(
        customer=customer,
        status='not confirmed',
        pay=pay,
        delivery=delivery,
        total=total,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order