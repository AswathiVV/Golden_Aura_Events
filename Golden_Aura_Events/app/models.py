from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.utils.timezone import now

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]


class DestinationWedding(models.Model):
    name = models.CharField(max_length=255) 
    about = models.TextField() 
    img = models.FileField()
    location = models.CharField(max_length=255) 
    package_price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return self.name
    
class ItemCategory(models.Model):
    img = models.FileField()
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    img = models.FileField()

    def __str__(self):
        return self.name    
  

class InvitationCategory(models.Model):
    img = models.FileField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 


class InvitationCard(models.Model):
    category = models.ForeignKey(InvitationCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price=models.IntegerField()
    img1 = models.FileField()
    img2 = models.FileField(blank=True, null=True)
    img3 = models.FileField(blank=True, null=True)
    img4 = models.FileField(blank=True, null=True)
    size = models.CharField(max_length=50) 

    def __str__(self):
        return self.name      
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20) 
    email = models.EmailField()

    def __str__(self):
        return self.name 

class BuyItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price=models.IntegerField()
    date = models.DateField()
    purchase_date = models.DateField(auto_now_add=True) 
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def get_total_price(self):
        return self.quantity * self.price
    

    def can_cancel(self):
        return (now().date() - self.purchase_date).days <= 2 and self.status == 'pending'



class BuyDesWedding(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    des = models.ForeignKey(DestinationWedding, on_delete=models.CASCADE)
    price=models.IntegerField()
    date = models.DateField()
    purchase_date = models.DateField(auto_now_add=True) 
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def can_cancel(self):
        return (now().date() - self.purchase_date).days <= 2 and self.status == 'pending'    
  

class BuyInv(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    inv = models.ForeignKey(InvitationCard, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price=models.IntegerField()
    date = models.DateField()
    message = models.TextField(blank=True, null=True)
    purchase_date = models.DateField(auto_now_add=True) 
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


    def total_price(self):
        return self.qty * self.price

    def can_cancel(self):
        return (now().date() - self.purchase_date).days <= 2 and self.status == 'pending'