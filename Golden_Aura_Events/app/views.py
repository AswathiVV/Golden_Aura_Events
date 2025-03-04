from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
import re
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
import razorpay
import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.utils import IntegrityError  
import math
import random
import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    
    if req.method == 'POST':
        uname = req.POST['uname']
        password = req.POST['password']
        data = authenticate(username=uname, password=password)
        if data:
            login(req, data)
            if data.is_superuser:
                req.session['shop'] = uname  
                return redirect(shop_home)
            else:
                req.session['user'] = uname  
                return redirect(user_home)
        else:
            messages.warning(req, "Invalid username or password")  
    return render(req, 'login.html') 



def OTP():
    digits = "0123456789"
    otp = "".join(random.choice(digits) for _ in range(6))
    return otp


def register(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        otp = OTP()  

        if User.objects.filter(email=email).exists():
            messages.error(req, "Email is already in use.")
            return redirect('shop_register')

        try:
            send_mail(
                'Your registration OTP',
                f"Your OTP for registration is: {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            print(f"OTP sent: {otp}") 
        except Exception as e:
            print(f"Error sending OTP: {e}") 
            messages.error(req, "Failed to send OTP. Please try again.")
            return redirect('shop_register')

        req.session['otp_data'] = {
            'name': name,
            'email': email,
            'password': password,
            'otp': otp
        }

        messages.success(req, "Registration successful. Please check your email for OTP.")
        return redirect(validate)  

    return render(req, 'register.html')


def validate(req):
    user_data = req.session.get('otp_data', {})

    if not user_data:
        messages.error(req, "Session expired. Please register again.")
        return redirect(register)

    name = user_data['name']
    email = user_data['email']
    password = user_data['password']
    otp = user_data['otp']

    if req.method == 'POST':
        uotp = req.POST['uotp']

        if uotp == otp:
            if User.objects.filter(username=email).exists(): 
                messages.error(req, "This email is already registered. Please log in.")
                return redirect(shop_login)

            try:
                User.objects.create_user(first_name=name, email=email, password=password, username=email)
                messages.success(req, "OTP verified successfully. You can now log in.")

                del req.session['otp_data']
                return redirect(shop_login)

            except IntegrityError:  
                messages.error(req, "This email is already registered. Please log in.")
                return redirect(shop_login)

        else:
            messages.error(req, "Invalid OTP. Please try again.")
            return redirect("validate")

    return render(req, 'validate.html', {'email': email})



# def shop_login(req):
#     if 'shop' in req.session:
#         return redirect(shop_home)
#     if 'user' in req.session:
#         return redirect(user_home)
#     else:
    
#         if req.method=='POST':
#             uname=req.POST['uname']
#             password=req.POST['password']
#             data=authenticate(username=uname,password=password)
#             if data:
#                 login(req,data)
#                 if data.is_superuser:
#                     req.session['shop']=uname      
#                     return redirect(shop_home)
#                 else:
#                     req.session['user']=uname      
#                     return redirect(user_home)
#             else:
#                 messages.warning(req,"invalid uname or password")  
#         return render(req,'login.html') 
     


# def register(req):
#     if req.method == 'POST':
#         name = req.POST.get('name', '').strip()
#         email = req.POST.get('email', '').strip()
#         password = req.POST.get('password', '').strip()

#         if not name or not email or not password:
#             messages.error(req, "All fields are required.")
#             return redirect(register)

#         email_regex = r'^[a-z][a-z0-9._%+-]*\d[a-z0-9._%+-]*@[a-z0-9.-]+\.[a-z]{2,}$'
#         if not re.fullmatch(email_regex, email): 
#             messages.error(req, "Invalid email format.")
#             return redirect(register)

#         if len(password) < 6:
#             messages.error(req, "Password must be at least 6 characters long.")
#             return redirect(register)
#         if not re.search(r'[A-Z]', password):
#             messages.error(req, "Password must contain at least one uppercase letter.")
#             return redirect(register)
#         if not re.search(r'\d', password):
#             messages.error(req, "Password must contain at least one number.")
#             return redirect(register)

#         if User.objects.filter(username=email).exists():
#             messages.warning(req, "User already exists.")
#             return redirect(register)

#         try:
#             user = User.objects.create_user(first_name=name, username=email, email=email, password=password)
#             user.save()

#             send_mail(
#                 'Golden Aura Events Registration',
#                 'Welcome to Golden Aura Events! Your account has been created successfully.',
#                 settings.EMAIL_HOST_USER,
#                 [email],
#                 fail_silently=False
#             )

#             messages.success(req, "Registration successful! Please log in.")
#             return redirect(shop_login)

#         except Exception as e:
#             messages.error(req, f"Registration failed: {str(e)}")
#             return redirect(register)

#     return render(req, 'register.html')

def shop_logout(req):
    logout(req)
    req.session.flush()              
    return redirect(shop_login)

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Message from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                message_body,
                settings.EMAIL_HOST_USER,
                ['goldenaurae@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "Your message has been sent successfully!")
        except:
            messages.error(request, "Failed to send your message. Please try again.")

        return redirect(contact_us) 

    return render(request, 'user/contact.html')


#--------------------- admin-------------------------------------------------------------------------------------------  
def shop_home(req):
    if 'shop' in req.session:
        return render(req,'shop/shop_home.html')
    else:
        return redirect(shop_login)
    
    
def add_deswedding(req):
    if req.method == 'POST':
        name = req.POST['name']
        about = req.POST['about']
        file = req.FILES['img']
        location = req.POST['location']
        package_price = req.POST['package_price']

        if not all([name, about, file, location, package_price]):
            return HttpResponse("All fields are required.", status=400)

        data = DestinationWedding.objects.create(
            name=name, 
            about=about, 
            img=file, 
            location=location, 
            package_price=package_price
        )
        
        data.save()
        return redirect(shop_home)  

    return render(req, 'shop/add_deswedding.html')

def add_category(req):
    if req.method == "POST":
        name = req.POST.get("name")
        price = req.POST.get("price") 
        img = req.FILES.get("img")

        if not all([name, price, img]):
            return HttpResponse("All fields are required.", status=400)

        category = ItemCategory.objects.create(name=name, price=price, img=img)
        category.save()
        return redirect(shop_home)  

    return render(req, "shop/add_item.html")

def add_item(req):
    if req.method == "POST":
        category_id = req.POST.get("category")
        name = req.POST.get("name")
        img = req.FILES.get("img")

        if not all([category_id, name, img]):
            return HttpResponse("All fields are required.", status=400)

        category = ItemCategory.objects.get(id=category_id)
        item = Item.objects.create(category=category, name=name, img=img)
        item.save()
        return redirect(shop_home) 

    categories = ItemCategory.objects.all()
    return render(req, "shop/add_item.html", {"categories": categories})


def add_invitation_category(req):
    if req.method == "POST":
        name = req.POST.get("name")
        img = req.FILES.get("img")

        if not all([name, img]):
            return HttpResponse("All fields are required.", status=400)

        category = InvitationCategory.objects.create(name=name, img=img)
        category.save()
        return redirect(shop_home) 

    categories = InvitationCategory.objects.all()
    return render(req, "shop/add_invitation.html", {"categories": categories})

def add_invitation_card(req):
    if req.method == "POST":
        category_id = req.POST.get("category")
        name = req.POST.get("name")
        price = req.POST.get("price")
        size = req.POST.get("size")
        img1 = req.FILES.get("img1")
        img2 = req.FILES.get("img2")
        img3 = req.FILES.get("img3")
        img4 = req.FILES.get("img4")

        if not all([category_id, name, price, size, img1]):
            return HttpResponse("All required fields must be filled.", status=400)

        category = InvitationCategory.objects.get(id=category_id)
        invitation_card = InvitationCard.objects.create(
            category=category, name=name, price=price, size=size,
            img1=img1, img2=img2, img3=img3, img4=img4
        )
        invitation_card.save()
        return redirect(shop_home)  

    categories = InvitationCategory.objects.all()
    return render(req, "shop/add_invitation.html", {"categories": categories})


def shop_destination_weddings(req):
    weddings = DestinationWedding.objects.all()
    return render(req, "shop/des_wedding.html", {"weddings": weddings})

def edit_wedding(req, wedding_id):
    wedding = get_object_or_404(DestinationWedding, pk=wedding_id)

    if req.method == 'POST':
        name = req.POST.get('name')
        location = req.POST.get('location')
        price = req.POST.get('package_price')
        about = req.POST.get('about')
        file = req.FILES.get('img')

        wedding.name = name
        wedding.location = location
        wedding.package_price = price
        wedding.about = about

        if file:
            wedding.img = file  

        wedding.save()

        return redirect(shop_destination_weddings) 

    return render(req, 'shop/edit_wedding.html', {'wedding': wedding})


def delete_wedding(req, wedding_id):
    get_object_or_404(DestinationWedding, id=wedding_id).delete()
    return redirect(shop_destination_weddings)


def category_view(request):
    categories = ItemCategory.objects.all()
    return render(request, 'shop/item_category.html', {'categories': categories})

def items_view(request, category_id):
    category = get_object_or_404(ItemCategory, id=category_id)
    items = Item.objects.filter(category=category)
    return render(request, 'shop/items.html', {'category': category, 'items': items})

# def shop_items(req):
#     categories = ItemCategory.objects.all()
#     items = Item.objects.all()
#     return render(req, 'shop/items.html', {'categories': categories, 'items': items})

def edit_category(req, category_id):
    category = get_object_or_404(ItemCategory, id=category_id)

    if req.method == "POST":
        category.name = req.POST.get("name")
        category.price = req.POST.get("price")
        if req.FILES.get("img"):
            category.img = req.FILES.get("img")
        category.save()
        return redirect(category_view)

    return render(req, "shop/edit_category.html", {"category": category})

def delete_category(req, category_id):
    category = get_object_or_404(ItemCategory, id=category_id)
    category.delete()
    return redirect(category_view)

def edit_item(req, item_id):
    item = get_object_or_404(Item, id=item_id)

    if req.method == "POST":
        item.name = req.POST.get("name")
        category_id = req.POST.get("category")
        item.category = get_object_or_404(ItemCategory, id=category_id)
        if req.FILES.get("img"):
            item.img = req.FILES.get("img")
        item.save()
        return redirect(category_view)

    return render(req, "shop/edit_item.html", {"item": item, "categories": ItemCategory.objects.all()})

def delete_item(req, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect(category_view)

# def shop_invitations(req):
#     categories = InvitationCategory.objects.all()
#     cards = InvitationCard.objects.all()
#     return render(req, "shop/invitations.html", {"categories": categories, "cards": cards})

def inv_cat_view(request):
    categories = InvitationCategory.objects.all()
    return render(request, 'shop/inv_category.html', {'categories': categories})

# View for managing cards inside a specific category
def inv_cards_view(request, category_id):
    category = get_object_or_404(InvitationCategory, id=category_id)
    cards = InvitationCard.objects.filter(category=category)
    return render(request, 'shop/invitation_cards.html', {'category': category, 'cards': cards})

def edit_invitation_category(req, category_id):
    category = get_object_or_404(InvitationCategory, id=category_id)

    if req.method == "POST":
        category.name = req.POST.get("name")
        if req.FILES.get("img"):
            category.img = req.FILES.get("img")
        category.save()
        return redirect(inv_cat_view)

    return render(req, "shop/edit_inv_category.html", {"category": category})

def delete_invitation_category(req, category_id):
    category = get_object_or_404(InvitationCategory, id=category_id)
    category.delete()
    return redirect(inv_cat_view)

# def edit_invitation_card(req, card_id):
#     card = get_object_or_404(InvitationCard, id=card_id)

#     if req.method == "POST":
#         card.name = req.POST.get("name")
#         card.price = req.POST.get("price")
#         card.size = req.POST.get("size")
#         if req.FILES.get("img1"):
#             card.img1 = req.FILES.get("img1")
#         card.save()
        
#         return redirect(inv_cards_view)

#     return render(req, "shop/edit_inv_card.html", {"card": card})

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

def edit_invitation_card(req, card_id):
    card = get_object_or_404(InvitationCard, id=card_id)

    if req.method == "POST":
        card.name = req.POST.get("name")
        card.price = req.POST.get("price")
        card.size = req.POST.get("size")

        if req.FILES.get("img1"):
            card.img1 = req.FILES.get("img1")
        if req.FILES.get("img2"):
            card.img2 = req.FILES.get("img2")
        if req.FILES.get("img3"):
            card.img3 = req.FILES.get("img3")
        if req.FILES.get("img4"):
            card.img4 = req.FILES.get("img4")

        card.save()
        
        # Ensure category_id is available
        category_id = card.category.id  # Assuming `card` has a `category` ForeignKey

        return redirect(reverse('inv_cards_view', args=[category_id]))  # Corrected redirect

    return render(req, "shop/edit_inv_card.html", {"card": card})


def delete_invitation_card(req, card_id):
    card = get_object_or_404(InvitationCard, id=card_id)
    card.delete()
    return redirect(inv_cards_view)


# def bookings(req):
#     user = User.objects.get(username=req.session['user'])

#     if user.is_superuser:
#         destination_bookings = BuyDesWedding.objects.all().order_by('-id')
#         invitation_bookings = BuyInv.objects.all().order_by('-id')
#         item_bookings = BuyItem.objects.all().order_by('-id')
#     else:
#         destination_bookings = BuyDesWedding.objects.filter(user=user).order_by('-id')
#         invitation_bookings = BuyInv.objects.filter(user=user).order_by('-id')
#         item_bookings = BuyItem.objects.filter(user=user).order_by('-id')

#     return render(req, 'user/view_bookings.html', {
#         'destination_bookings': destination_bookings,
#         'invitation_bookings': invitation_bookings,
#         'item_bookings': item_bookings
#     })


# def bookings(req):
#     if not req.user.is_superuser:
#         return redirect('login') 

#     destination_bookings = BuyDesWedding.objects.all().order_by('-id')
#     invitation_bookings = BuyInv.objects.all().order_by('-id')
#     item_bookings = BuyItem.objects.all().order_by('-id')

#     return render(req, 'shop/bookings.html', {
#         'destination_bookings': destination_bookings,
#         'invitation_bookings': invitation_bookings,
#         'item_bookings': item_bookings
#     })


def admin_bookings(req):
    users = User.objects.all()
    
    buy_items = BuyItem.objects.select_related('user', 'item', 'address', 'order').all().order_by('-purchase_date')
    buy_weddings = BuyDesWedding.objects.select_related('user', 'des', 'address', 'order').all().order_by('-purchase_date')
    buy_invites = BuyInv.objects.select_related('user', 'inv', 'address', 'order').all().order_by('-purchase_date')
    
    total_profit = (
        sum(item.get_total_price() for item in buy_items) +
        sum(wed.price for wed in buy_weddings) +
        sum(inv.total_price() for inv in buy_invites)
    )

    return render(req, 'shop/admin_bookings.html', {
        'users': users,
        'buy_items': buy_items,
        'buy_weddings': buy_weddings,
        'buy_invites': buy_invites,
        'total_profit': total_profit
    })


def cancel_order(req, order_id, order_type):
    """
    Cancels an order based on its type.
    order_type should be 'item', 'wedding', or 'inv'.
    """
    if order_type == "item":
        order = get_object_or_404(BuyItem, pk=order_id)
    elif order_type == "wedding":
        order = get_object_or_404(BuyDesWedding, pk=order_id)
    elif order_type == "inv":
        order = get_object_or_404(BuyInv, pk=order_id)
    else:
        return redirect("admin_bookings")  # Invalid type, do nothing

    order.delete()
    return redirect("admin_bookings")


# def confirm_order(request, order_id, order_type):
#     if order_type == "item":
#         order = get_object_or_404(BuyItem, pk=order_id)
#         item_name = order.item.name
#     elif order_type == "wedding":
#         order = get_object_or_404(BuyDesWedding, pk=order_id)
#         item_name = order.des.name
#     elif order_type == "inv":
#         order = get_object_or_404(BuyInv, pk=order_id)
#         item_name = order.inv.name
#     else:
#         return redirect(admin_bookings)  

#     if not order.is_confirmed:
#         order.is_confirmed = True
#         order.save()

#         subject = "Order Confirmation"
#         message = f"Dear {order.user.first_name},\n\nYour order ({item_name}) has been confirmed. Thank you for shopping with us!\n\nBest regards,\nGolden Aura Events Team"

#         recipient_email = order.user.email  

#         try:
#             send_mail(
#                 subject,
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [recipient_email],
#                 fail_silently=False,
#             )
#         except Exception as e:
#             print(f"Email sending failed: {e}")

#     return redirect("admin_bookings")


# def confirm_order(request, order_id, order_type):
#     if order_type == "item":
#         order = get_object_or_404(BuyItem, pk=order_id)
#         item_name = order.item.name
#     elif order_type == "wedding":
#         order = get_object_or_404(BuyDesWedding, pk=order_id)
#         item_name = order.des.name
#     elif order_type == "inv":
#         order = get_object_or_404(BuyInv, pk=order_id)
#         item_name = order.inv.name
#     else:
#         print("Invalid order type!") 
#         return redirect("admin_bookings")

#     if not order.is_confirmed:
#         order.is_confirmed = True
#         order.save()

#         if not order.user or not order.user.email:
#             print("Error: User does not have an email address!")  
#             return redirect("admin_bookings")

#         recipient_email = order.user.email
#         print(f"Attempting to send email to: {recipient_email}")  

#         subject = "Order Confirmation"
#         message = f"""
#         Dear {order.user.first_name},

#         Your order ({item_name}) has been confirmed.
#         Thank you for choosing Golden Aura Events!

#         Best regards,
#         Golden Aura Events Team
#         """

#         try:
#             send_mail(
#                 subject,
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [recipient_email],
#                 fail_silently=False,
#             )
#             print("Email sent successfully!")  
#         except Exception as e:
#             print(f"Email sending failed: {e}")  

#     return redirect("admin_bookings")
def confirm_order(request, order_id, order_type):
    if order_type == "item":
        order = get_object_or_404(BuyItem, pk=order_id)
        item_name = order.item.name  # Use item
    elif order_type == "wedding":
        order = get_object_or_404(BuyDesWedding, pk=order_id)
        item_name = order.des.name  # Use des
    elif order_type == "inv":
        order = get_object_or_404(BuyInv, pk=order_id)
        item_name = order.inv.name  # Use inv
    else:
        print("Invalid order type!")  
        return redirect("admin_bookings")

    if not order.is_confirmed:
        order.is_confirmed = True
        order.save()

        if not order.user or not order.user.email:
            print("Error: User does not have an email address!")  
            return redirect("admin_bookings")

        recipient_email = order.user.email
        print(f"Attempting to send email to: {recipient_email}")  

        subject = "Order Confirmation"
        message = f"""
        Dear {order.user.first_name},

        Your order ({item_name}) has been confirmed.
        Thank you for choosing Golden Aura Events!

        Best regards,
        Golden Aura Events Team
        """

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient_email],
                fail_silently=False,
            )
            print("Email sent successfully!")  
        except Exception as e:
            print(f"Email sending failed: {e}")  

    return redirect("admin_bookings")


def toggle_confirmation(request, order_id, order_type):
    if order_type == "item":
        order = get_object_or_404(BuyItem, pk=order_id)
        item_name = order.item.name
    elif order_type == "wedding":
        order = get_object_or_404(BuyDesWedding, pk=order_id)
        item_name = order.des.name
    elif order_type == "inv":
        order = get_object_or_404(BuyInv, pk=order_id)
        item_name = order.inv.name
    else:
        return redirect("admin_bookings")  

    if not order.is_confirmed:
        order.is_confirmed = True
        order.save()
        print(f" Order {order_id} confirmed!")  # Debugging

        if not order.user or not order.user.email:
            print(" Error: User does not have an email address!")
            return redirect("admin_bookings")

        recipient_email = order.user.email
        print(f"📧 Attempting to send email to: {recipient_email}")  

        subject = "Order Confirmation"
        message = f"""
        Dear {order.user.first_name},

        Your order ({item_name}) has been confirmed.
        Thank you for choosing Golden Aura Events!

        Best regards,
        Golden Aura Events Team
        """

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient_email],
                fail_silently=False,
            )
            print("Email sent successfully!")  
        except Exception as e:
            print(f" Email sending failed: {e}")  

    return redirect(admin_bookings)


# #------------------------------------- User--------------------------------------------------------------

def user_home(req):
    if 'user' in req.session:
        return render(req,'user/user_home.html')  
    else:
        return redirect(shop_login)
    
def about(req):
    return render(req,'user/about.html')    

def contact(req):
    return render(req,'user/contact.html')
    

def destination_wedding(request):
    des_list = DestinationWedding.objects.all()  
    paginator = Paginator(des_list, 9)  

    page_number = request.GET.get('page')  
    des = paginator.get_page(page_number)  

    return render(request, 'user/destination_wedding.html', {'des': des})
    

def view_des_wed(req,id):
     if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        des=DestinationWedding.objects.get(pk=id)
          
        return render(req,'user/des_wed_details.html',{'des':des}) 
     else:
         return redirect(shop_home) 

     
def invitation(request):
    categories = InvitationCategory.objects.all()
    invitation_cards = InvitationCard.objects.all()
    return render(request, 'user/invitation.html', {'categories': categories, 'invitation_cards': invitation_cards})

def invitation_detail(request, id):  
    card = get_object_or_404(InvitationCard, id=id)
    return render(request, 'user/invitation_detail.html', {'card': card})

def item(req):
    categories = ItemCategory.objects.all()
    items = Item.objects.all()
    return render(req, 'user/item_categories.html', {'categories': categories, 'items': items})


def buy_des(req, id):
    des = get_object_or_404(DestinationWedding, pk=id)  
    return redirect(des_address_page, id=id)

def buy_inv(req, id):
    card = get_object_or_404(InvitationCard, pk=id)  
    return redirect(invitation_address_page, id=id)


def buy_item(req, id):
    item = get_object_or_404(Item, pk=id)  
    return redirect(items_address_page, id=id)

def view_bookings(req):
    user = get_object_or_404(User, username=req.session.get('user'))

    items = BuyItem.objects.filter(user=user).select_related('item').order_by('-id')
    weddings = BuyDesWedding.objects.filter(user=user).select_related('des').order_by('-id')
    invitations = BuyInv.objects.filter(user=user).select_related('inv').order_by('-id')

    for booking in items:
        booking.total_price = booking.price * booking.quantity  

    for booking in invitations:
        booking.total_price = booking.price * booking.qty  

    for booking in weddings:
        booking.total_price = booking.price  # No quantity field, so just assign price

    context = {
        'items': items,
        'weddings': weddings,
        'invitations': invitations,
    }
    return render(req, 'user/view_bookings.html', context)


def user_orders(request):
    user = get_object_or_404(User, username=request.session.get('user'))

    items = BuyItem.objects.filter(user=user).select_related('item').order_by('-id')
    weddings = BuyDesWedding.objects.filter(user=user).select_related('des').order_by('-id')
    invitations = BuyInv.objects.filter(user=user).select_related('inv').order_by('-id')

    for order in items:
        print(f"Item Order ID: {order.id}, Is Confirmed: {order.is_confirmed}")
    for order in weddings:
        print(f"Wedding Order ID: {order.id}")
    for order in invitations:
        print(f"Invitation Order ID: {order.id}")

    return render(request, 'user/view_bookings.html', {
        'items': items,
        'weddings': weddings,
        'invitations': invitations
    })


def delete_order(req, id):
    order = BuyItem.objects.filter(pk=id).first()
    if not order:
        order = BuyDesWedding.objects.filter(pk=id).first()
    if not order:
        order = BuyInv.objects.filter(pk=id).first()

    if order:
        order.delete()
    
    return redirect('view_bookings')  


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'user/profile.html', {'profile': profile, 'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address_text = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        if name and address_text and phone_number:
            address = Address.objects.create(
                user=request.user,
                name=name,
                address=address_text,
                phone_number=phone_number
            )

            profile, created = Profile.objects.get_or_create(user=request.user)
            if not profile.primary_address:
                profile.primary_address = address
                profile.save()

            messages.success(request, "Address added successfully.")
            return redirect('profile_view')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'user/profile.html')

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        address_text = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        if name and address_text and phone_number:
            address.name = name
            address.address = address_text
            address.phone_number = phone_number
            address.save()

            messages.success(request, "Address updated successfully.")
            return redirect('profile_view')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'user/profile.html', {'address': address})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    profile = get_object_or_404(Profile, user=request.user)

    if profile.primary_address == address:
        profile.primary_address = None
        profile.save()

    address.delete()
    messages.success(request, "Address deleted successfully.")
    return redirect(profile_view)


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('login')
    
    return render(request, "user/profile.html")



@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get("first_name", "").strip()
        username = request.POST.get("username", "").strip()

        if not first_name or not username:
            messages.error(request, "Both fields are required.")
            return render(request, "user/profile.html", {"user": user})

        try:
            validate_email(username)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return render(request, "user/profile.html", {"user": user})

        if user.username != username and user.__class__.objects.filter(username=username).exists():
            messages.error(request, "This email is already in use.")
            return render(request, "user/profile.html", {"user": user})

        user.first_name = first_name
        user.username = username
        user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile_view")

    return render(request, "user/profile.html", {"user": request.user})



# ________________________________________________________________________________________________________


def invitation_address_page(req, id):
    card = get_object_or_404(InvitationCard, pk=id)
    user = req.user
    
    user_address = Address.objects.filter(user=user).order_by('-id').first()

    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')
        quantity = int(req.POST.get('qty_card', 1))

        if user_address:
            user_address.name = name
            user_address.address = address
            user_address.phone_number = phone_number
            user_address.save()
        else:
            user_address = Address.objects.create(user=user, name=name, address=address, phone_number=phone_number)

        req.session['invitation_card'] = id
        req.session['quantity'] = quantity

        return redirect('invitation_order_payment')

    return render(req, 'user/order.html', {'card': card, 'user_address': user_address})

@login_required
def invitation_order_payment(req):
    if 'invitation_card' not in req.session:
        messages.error(req, "Invalid session. Please select an invitation card first.")
        return redirect('invitation_address_page', id=req.session.get('invitation_card', 1))  

    user = req.user
    invitation = get_object_or_404(InvitationCard, id=req.session['invitation_card'])
    
    qty = int(req.session.get('quantity', 1))  
    price_per_card = invitation.price  
    total_amount = price_per_card * qty 

    print(f"DEBUG: Invitation Price from DB: {invitation.price}")
    print(f"DEBUG: Quantity from session: {qty}")
    print(f"DEBUG: Total Amount Calculated: {total_amount}")


    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = razorpay_client.order.create({
        "amount": int(total_amount) * 100,  
        "currency": "INR",
        "payment_capture": "1"
    })

    order = Order.objects.create(
        user=user,
        price=total_amount,  
        provider_order_id=razorpay_order['id']
    )

    address = Address.objects.filter(user=user).order_by('-id').first()

    BuyInv.objects.create(
        user=user,
        inv=invitation,
        qty=qty,  
        price=total_amount,
        date=timezone.now().date(), 
        purchase_date=timezone.now().date(),
        address=address,
        order=order  
    )

    req.session['order_id'] = order.pk  

    return render(req, "user/payment.html", {
        "callback_url": "http://127.0.0.1:8000/callback/",
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order": order,
        "qty": qty,  
        "price_per_card": price_per_card,  
        "total_amount": total_amount  
    })


@login_required
def des_address_page(req, id):
    des = get_object_or_404(DestinationWedding, id=id)
    user = req.user  

    user_address = Address.objects.filter(user=user).order_by('-id').first()

    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')

        if user_address:
            Address.objects.filter(user=user).update(
                name=name, address=address, phone_number=phone_number, email=user.email
        )
        else:
            Address.objects.create(
                user=user, name=name, address=address, phone_number=phone_number, email=user.email
        )



        req.session['wedding'] = des.id  

        return redirect(des_order_payment)  

    return render(req, 'user/order.html', {
        'des': des,
        'user_address': user_address  
    })

@login_required
def des_order_payment(req):
    if 'wedding' not in req.session:
        messages.error(req, "Invalid session. Please select a wedding package first.")
        return redirect('des_address_page', id=req.session.get('wedding', 1)) 

    user = req.user
    wedding = get_object_or_404(DestinationWedding, id=req.session['wedding'])
    
    total_amount = wedding.package_price 

    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = razorpay_client.order.create({
        "amount": int(total_amount) * 100,  
        "currency": "INR",
        "payment_capture": "1"
    })

    order = Order.objects.create(
        user=user,
        price=total_amount,  
        provider_order_id=razorpay_order['id']
    )

    address = Address.objects.filter(user=user).order_by('-id').first()

    BuyDesWedding.objects.create(
        user=user,
        des=wedding,
        price=total_amount,
        date=timezone.now().date(), 
        purchase_date=timezone.now().date(),
        address=address,
        order=order  
    )

    req.session['order_id'] = order.pk  

    return render(req, "user/payment.html", {
        "callback_url": "http://127.0.0.1:8000/callback/",
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order": order,
    })


@login_required
def items_address_page(req, item_ids):
    item_ids_list = item_ids.split(',')
    items = Item.objects.filter(id__in=item_ids_list)
    user = req.user
    user_address = Address.objects.filter(user=user).order_by('-id').first()  

    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')

        if user_address:
            Address.objects.filter(id=user_address.id).update(name=name, address=address, phone_number=phone_number)
        else:
            Address.objects.create(user=user, name=name, address=address, phone_number=phone_number)

        req.session['item_ids'] = item_ids
        req.session['quantities'] = {item.id: int(req.POST.get(f'qty_{item.id}', 1)) for item in items}

        return redirect('items_order_payment')

    return render(req, 'user/order.html', {'items': items, 'user_address': user_address})


@login_required
def items_order_payment(req):
    user = req.user
    item_ids_list = req.session.get('item_ids', '').split(',')
    quantities = req.session.get('quantities', {})
    items = Item.objects.filter(id__in=item_ids_list)

    total_amount = sum(item.category.price * quantities.get(str(item.id), 1) for item in items)

    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = razorpay_client.order.create({
        "amount": int(total_amount * 100),
        "currency": "INR",
        "payment_capture": "1"
    })

    order = Order.objects.create(user=user, price=total_amount, provider_order_id=razorpay_order['id'])
    req.session['order_id'] = order.pk

    return render(req, "user/payment.html", {
        "callback_url": "http://127.0.0.1:8000/callback/",
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order": order,
    })

from django.utils.timezone import now

@login_required
def pay(req):
    user = req.user
    order_id = req.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id)
    
    user_address = Address.objects.filter(user=user).order_by('-id').first()
    if not user_address:
        messages.error(req, "Please add an address before proceeding to payment.")
        return redirect('items_address_page') 

    if 'item_ids' in req.session:
        item_ids_list = req.session.get('item_ids', '').split(',')
        quantities = req.session.get('quantities', {})
        items = Item.objects.filter(id__in=item_ids_list)

        for item in items:
            BuyItem.objects.create(
                user=user,
                item=item,
                quantity=quantities.get(str(item.id), 1),
                price=item.category.price,
                order=order,
                address=user_address,
                date=now()
            )

    return redirect(view_bookings)


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id

        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
        else:
            order.status = PaymentStatus.FAILURE

        order.save()
        return redirect(pay)
    

    else:
        payment_data = json.loads(request.POST.get("error[metadata]", "{}"))
        provider_order_id = payment_data.get("order_id", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.status = PaymentStatus.FAILURE
        order.save()

        return redirect(pay)

