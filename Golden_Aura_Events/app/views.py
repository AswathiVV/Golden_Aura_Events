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
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    else:
    
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
                    req.session['shop']=uname      
                    return redirect(shop_home)
                else:
                    req.session['user']=uname      
                    return redirect(user_home)
            else:
                messages.warning(req,"invalid uname or password")  
        return render(req,'login.html') 
    
def shop_logout(req):
    logout(req)
    req.session.flush()              
    return redirect(shop_login) 

# def  register(req):
#      if req.method=='POST':
#         name=req.POST['name']       
#         email=req.POST['email']
#         password=req.POST['password']
#         send_mail('Golden Aura Events registration', 'Welcome to Golden Aura Events! Your account has been created successfully', settings.EMAIL_HOST_USER, [email])

#         try:
#             data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
#             data.save()
#             return redirect(shop_login)
#         except:
#             messages.warning(req,"user details already exits")
#             return redirect(register)
#      else:
#          return render(req,'register.html')


# def register(req):
#     if req.method == 'POST':
#         name = req.POST.get('name', '').strip()
#         email = req.POST.get('email', '').strip()
#         password = req.POST.get('password', '').strip()

#         if not name or not email or not password:
#             messages.error(req, "All fields are required.")
#             return redirect(register)

#         email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#         if not re.match(email_regex, email):
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

#             # Send welcome email
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
     
# import re
# from django.contrib import messages
# from django.shortcuts import redirect, render
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth.models import User

def register(req):
    if req.method == 'POST':
        name = req.POST.get('name', '').strip()
        email = req.POST.get('email', '').strip()
        password = req.POST.get('password', '').strip()

        if not name or not email or not password:
            messages.error(req, "All fields are required.")
            return redirect(register)

        email_regex = r'^[a-z][a-z0-9._%+-]*\d[a-z0-9._%+-]*@[a-z0-9.-]+\.[a-z]{2,}$'
        if not re.fullmatch(email_regex, email): 
            messages.error(req, "Invalid email format.")
            return redirect(register)

        if len(password) < 6:
            messages.error(req, "Password must be at least 6 characters long.")
            return redirect(register)
        if not re.search(r'[A-Z]', password):
            messages.error(req, "Password must contain at least one uppercase letter.")
            return redirect(register)
        if not re.search(r'\d', password):
            messages.error(req, "Password must contain at least one number.")
            return redirect(register)

        if User.objects.filter(username=email).exists():
            messages.warning(req, "User already exists.")
            return redirect(register)

        try:
            user = User.objects.create_user(first_name=name, username=email, email=email, password=password)
            user.save()

            send_mail(
                'Golden Aura Events Registration',
                'Welcome to Golden Aura Events! Your account has been created successfully.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            messages.success(req, "Registration successful! Please log in.")
            return redirect(shop_login)

        except Exception as e:
            messages.error(req, f"Registration failed: {str(e)}")
            return redirect(register)

    return render(req, 'register.html')

# from django.shortcuts import render, redirect
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib import messages

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


def shop_items(req):
    categories = ItemCategory.objects.all()
    items = Item.objects.all()
    return render(req, 'shop/items.html', {'categories': categories, 'items': items})

def edit_category(req, category_id):
    category = get_object_or_404(ItemCategory, id=category_id)

    if req.method == "POST":
        category.name = req.POST.get("name")
        category.price = req.POST.get("price")
        if req.FILES.get("img"):
            category.img = req.FILES.get("img")
        category.save()
        return redirect(shop_items)

    return render(req, "shop/edit_category.html", {"category": category})

def delete_category(req, category_id):
    category = get_object_or_404(ItemCategory, id=category_id)
    category.delete()
    return redirect(shop_items)

def edit_item(req, item_id):
    item = get_object_or_404(Item, id=item_id)

    if req.method == "POST":
        item.name = req.POST.get("name")
        category_id = req.POST.get("category")
        item.category = get_object_or_404(ItemCategory, id=category_id)
        if req.FILES.get("img"):
            item.img = req.FILES.get("img")
        item.save()
        return redirect(shop_items)

    return render(req, "shop/edit_item.html", {"item": item, "categories": ItemCategory.objects.all()})

def delete_item(req, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect(shop_items)

def shop_invitations(req):
    categories = InvitationCategory.objects.all()
    cards = InvitationCard.objects.all()
    return render(req, "shop/invitations.html", {"categories": categories, "cards": cards})

def edit_invitation_category(req, category_id):
    category = get_object_or_404(InvitationCategory, id=category_id)

    if req.method == "POST":
        category.name = req.POST.get("name")
        if req.FILES.get("img"):
            category.img = req.FILES.get("img")
        category.save()
        return redirect(shop_invitations)

    return render(req, "shop/edit_inv_category.html", {"category": category})

def delete_invitation_category(req, category_id):
    category = get_object_or_404(InvitationCategory, id=category_id)
    category.delete()
    return redirect(shop_invitations)

def edit_invitation_card(req, card_id):
    card = get_object_or_404(InvitationCard, id=card_id)

    if req.method == "POST":
        card.name = req.POST.get("name")
        card.price = req.POST.get("price")
        card.size = req.POST.get("size")
        if req.FILES.get("img1"):
            card.img1 = req.FILES.get("img1")
        card.save()
        
        return redirect(shop_invitations)

    return render(req, "shop/edit_inv_card.html", {"card": card})

def delete_invitation_card(req, card_id):
    card = get_object_or_404(InvitationCard, id=card_id)
    card.delete()
    return redirect(shop_invitations)


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


def bookings(req):
    if not req.user.is_superuser:
        return redirect('login') 

    destination_bookings = BuyDesWedding.objects.all().order_by('-id')
    invitation_bookings = BuyInv.objects.all().order_by('-id')
    item_bookings = BuyItem.objects.all().order_by('-id')

    return render(req, 'shop/bookings.html', {
        'destination_bookings': destination_bookings,
        'invitation_bookings': invitation_bookings,
        'item_bookings': item_bookings
    })


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

    
# def destination_wedding(request):
#         des = DestinationWedding.objects.all() 
#         return render(request, 'user/destination_wedding.html', {'des': des})
    

def destination_wedding(request):
    des_list = DestinationWedding.objects.all()  # Fetch all destination weddings
    paginator = Paginator(des_list, 9)  # Show 9 items per page

    page_number = request.GET.get('page')  # Get the current page number from URL
    des = paginator.get_page(page_number)  # Get paginated objects

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


# def invitation_address_page(request, id):
#     card = InvitationCard.objects.get(pk=id)

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         phone_number = request.POST.get('phone_number')
#         email = request.POST.get('email')
#         order_date = request.POST.get('date')
#         order=Order.objects.get(pk=request.session['order_id'])


#         quantity = request.POST.get('qty_card', '1')  
#         try:
#             quantity = int(quantity)
#         except ValueError:
#             quantity = 1  

#         user_address = Address(user=request.user, name=name, address=address, phone_number=phone_number, email=email)
#         user_address.save()

#         price = card.price

#         buy = BuyInv(
#             user=request.user,
#             inv=card,
#             qty=quantity,  
#             price=price,
#             date=order_date,
#             address=user_address,
#             order=order

#         )
#         buy.save()

#         return redirect(view_bookings)
    

#     return render(request, 'user/order.html', {'card': card})

@login_required
def invitation_address_page(request, id):
    card = InvitationCard.objects.get(pk=id)
    user_address = Address.objects.filter(user=request.user).first()

    if request.method == 'POST':
        use_saved_address = request.POST.get('use_saved_address')

        if use_saved_address == 'yes' and user_address:
            selected_address = user_address
        else:
            name = request.POST.get('name')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')

            selected_address = Address(
                user=request.user,
                name=name,
                address=address,
                phone_number=phone_number,
                email=email
            )
            selected_address.save()

        quantity = int(request.POST.get('qty_card', 1))
        price = card.price

        buy_inv = BuyInv(
            user=request.user,
            inv=card,
            qty=quantity,
            price=price,
            date=request.POST.get('date'),
            address=selected_address
        )
        buy_inv.save()

        return redirect('view_bookings')  # Redirect after saving

    return render(request, 'user/order.html', {'card': card, 'user_address': user_address})


# def des_address_page(req, id):
#     des = DestinationWedding.objects.get(id=id)

#     if req.method == 'POST':
#         name = req.POST.get('name')
#         address = req.POST.get('address')
#         phone_number = req.POST.get('phone_number')
#         email = req.POST.get('email')
#         wedding_date = req.POST.get('date')  

#         user_address = Address(user=req.user, name=name, address=address, phone_number=phone_number, email=email)
#         user_address.save()

#         buy = BuyDesWedding(user=req.user, des=des, price=des.package_price, date=wedding_date, address=user_address)
#         buy.save()

#         return redirect(view_bookings)

#     return render(req, 'user/order.html', {'des': des})

@login_required
def des_address_page(request, id):
    des = DestinationWedding.objects.get(id=id)
    user_address = Address.objects.filter(user=request.user).first()  # Get saved address if available

    if request.method == 'POST':
        use_saved_address = request.POST.get('use_saved_address')

        if use_saved_address == 'yes' and user_address:
            selected_address = user_address  # Use saved address
        else:
            name = request.POST.get('name')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')

            selected_address = Address(
                user=request.user,
                name=name,
                address=address,
                phone_number=phone_number,
                email=email
            )
            selected_address.save()  

        wedding_date = request.POST.get('date')


        buy = BuyDesWedding(
            user=request.user,
            des=des,
            price=des.package_price,
            date=wedding_date,
            address=selected_address
        )
        buy.save()

        return redirect('view_bookings')

    return render(request, 'user/order.html', {'des': des, 'user_address': user_address})


@login_required
def items_address_page(request, item_ids):
    item_ids = item_ids.split(',')  
    items = Item.objects.select_related('category').filter(id__in=item_ids)

    user_address = Address.objects.filter(user=request.user).first()

    if request.method == 'POST':
        use_saved_address = request.POST.get('use_saved_address')

        if use_saved_address == 'yes' and user_address:
            selected_address = user_address
        else:
            name = request.POST.get('name')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')

            selected_address = Address(
                user=request.user,
                name=name,
                address=address,
                phone_number=phone_number,
                email=email
            )
            selected_address.save()

        for item in items:
            quantity = int(request.POST.get(f'qty_{item.id}', 1))
            price = item.category.price

            order = BuyItem(
                user=request.user,
                item=item,
                quantity=quantity,
                price=price,
                date=request.POST.get('date'),
                address=selected_address  
            )
            order.save()

        return redirect('view_bookings')  

    return render(request, 'user/order.html', {'items': items, 'user_address': user_address})



def view_bookings(req):
    user = User.objects.get(username=req.session['user'])
    destination_bookings = BuyDesWedding.objects.filter(user=user)[::-1]
    invitation_bookings = BuyInv.objects.filter(user=user)[::-1]
    item_bookings = BuyItem.objects.filter(user=user)[::-1]


    return render(req, 'user/view_bookings.html', {
        'destination_bookings': destination_bookings,
        'invitation_bookings': invitation_bookings,
        'item_bookings': item_bookings
    })


def cancel_booking(request, booking_type, booking_id):
    if booking_type == "wedding":
        booking = get_object_or_404(BuyDesWedding, id=booking_id)
    elif booking_type == "invitation":
        booking = get_object_or_404(BuyInv, id=booking_id)
    elif booking_type == "item":
        booking = get_object_or_404(BuyItem, id=booking_id)
    else:
        messages.error(request, "Invalid booking type.")
        return redirect("view_bookings") 

    booking.status = "cancelled"
    booking.save()

    messages.success(request, "Your booking has been cancelled.")
    
    return redirect(view_bookings) 



# def invitation_address_page(request, id):
#     card = get_object_or_404(InvitationCard, pk=id)

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         phone_number = request.POST.get('phone_number')
#         email = request.POST.get('email')
#         order_date = request.POST.get('date')
#         quantity = int(request.POST.get('qty_card', '1') or 1)

#         user_address = Address.objects.create(
#             user=request.user, name=name, address=address,
#             phone_number=phone_number, email=email
#         )

#         request.session['service_type'] = 'invitation'
#         request.session['service_id'] = id
#         request.session['quantity'] = quantity

#         return redirect('order_payment', service_type='invitation', id=id)

#     return render(request, 'user/order.html', {'card': card})


# def des_address_page(request, id):
#     des = get_object_or_404(DestinationWedding, pk=id)

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         phone_number = request.POST.get('phone_number')
#         email = request.POST.get('email')

#         user_address = Address.objects.create(
#             user=request.user, name=name, address=address,
#             phone_number=phone_number, email=email
#         )

#         request.session['service_type'] = 'wedding'
#         request.session['service_id'] = id

#         # return redirect('order_payment', service_type='wedding', id=id)
#         # return redirect(order_payment, service_type='wedding', id=id)
#         return redirect('order_payment', obj_type='wedding', obj_id=id)


#     return render(request, 'user/order.html', {'des': des})


# def items_address_page(request, item_ids):
#     item_ids = item_ids.split(',')
#     items = Item.objects.filter(id__in=item_ids)

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         phone_number = request.POST.get('phone_number')
#         email = request.POST.get('email')

#         user_address = Address.objects.create(
#             user=request.user, name=name, address=address,
#             phone_number=phone_number, email=email
#         )

#         request.session['service_type'] = 'item'
#         request.session['service_ids'] = item_ids

#         return redirect('order_payment', service_type='item', id=item_ids[0])

#     return render(request, 'user/order.html', {'items': items})




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
