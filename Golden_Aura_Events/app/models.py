from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

    
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img1 = models.FileField()
    img2 = models.FileField(blank=True, null=True)
    img3 = models.FileField(blank=True, null=True)
    img4 = models.FileField(blank=True, null=True)
    size = models.CharField(max_length=50) 

    def __str__(self):
        return self.name  
    
    
    
class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    wedding = models.ForeignKey(DestinationWedding, on_delete=models.CASCADE,null=True) 
    invitation = models.ForeignKey(InvitationCard, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=255)  
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)  
    address = models.TextField(default="Not Provided")
    purchase_date = models.DateField(auto_now_add=True)  
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )      
    def is_cancellable(self):
        return (date.today() - self.purchase_date) <= timedelta(days=2)
    
    def calculate_total_invitation(self):
        if self.invitation:
            return self.invitation.price  
        return 0
    
    def calculate_total(self):
        total = 0
        for buy_item in self.buyitem_set.all():
            total += buy_item.calculate_item_price()
        if self.invitation:
            total += self.invitation.price
        return total

class Customization(models.Model):
    buy = models.OneToOneField(Buy, on_delete=models.CASCADE)
    groom_name = models.CharField(max_length=100)
    bride_name = models.CharField(max_length=100)
    wedding_date = models.DateField()
    location = models.TextField()
    guest_count = models.PositiveIntegerField(default=1) 
    time = models.TimeField()
    additional_notes = models.TextField(blank=True, null=True)
    
    def calculate_total_price(self):
        if self.buy and self.buy.invitation:
            return self.buy.invitation.price * self.guest_count
        return 0

    def __str__(self):
        return f"Customization for {self.groom_name} & {self.bride_name}"


class BuyItem(models.Model):
    buy = models.ForeignKey(Buy, on_delete=models.CASCADE, related_name="buyitem_set")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def calculate_item_price(self):
        return self.item.category.price * self.quantity

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"

    
