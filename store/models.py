from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
###########################################################################################################

class Category(models.Model):
    name = models.CharField(max_length=20, null = True)

    def __str__(self):
        return self.name
    
class Category2(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=20, null = True)

    def __str__(self):
        return self.name
    
###########################################################################################################

class Product(models.Model):
    pname = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=200, blank=True, default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    category = models.ManyToManyField(Category)
    category2 = models.ManyToManyField(Category2, default=False, blank=True)
    rating = models.FloatField(default=0)

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
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null = True)

    def __str__(self):
        return str(self.id)
    
###########################################################################################################
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    qunatity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

###########################################################################################################
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null = True)
    city = models.CharField(max_length=200, null = True)
    state = models.CharField(max_length=200, null = True)
    zipcode = models.CharField(max_length=200, null = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
###########################################################################################################
