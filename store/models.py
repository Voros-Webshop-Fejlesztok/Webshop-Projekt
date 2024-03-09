from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    follows = models.ManyToManyField("self", related_name='following',symmetrical=False, blank=True)
    followers = models.ManyToManyField("self", related_name='followed_by',symmetrical=False, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    last_friend = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def friends(self):
        user_followers = self.followers.all()
        user_following = self.follows.all()

        return user_followers.intersection(user_following)
    
###########################################################################################################

class Category(models.Model):
    name = models.CharField(max_length=20, null = True)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=20, null = True)

    def __str__(self):
        return self.name
    
###########################################################################################################

class Product(models.Model):
    pname = models.CharField(max_length=200, null=True)
    price = models.IntegerField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=200, blank=True, default='')
    stock = models.IntegerField(blank=True, default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    category = models.ManyToManyField(Category)
    rating = models.FloatField(default=0)
    darkweb = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.pname
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

###########################################################################################################
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null = True)
    transaction_id = models.CharField(max_length=200, null = True)
    pay =  models.CharField(max_length=10, blank=True, null=True)
    delivery = models.CharField(max_length=10, blank=True, null=True)
    total = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.id}. rendelés '
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
###########################################################################################################
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order} - {self.quantity} db {self.product} '

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

###########################################################################################################
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null = True)
    city= models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null = True)
    zipcode = models.CharField(max_length=200, null = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city + ' ' + self.address
class BillingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null = True)
    city= models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null = True)
    zipcode = models.CharField(max_length=200, null = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city + ' ' + self.address
    
##############################################################################
    
class Post(models.Model):
    profile = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    body = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Customer, related_name='liked_by', symmetrical=False, blank=True)

    def number_of_likes(self):
        return self.likes.count() - 1

    def __str__(self):
        return f"{self.profile} " + f"{self.created:%Y-%m-%d %H:%M}"
    
class Message(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    sent_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.sent_date})"