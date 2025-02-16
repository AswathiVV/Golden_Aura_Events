from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone


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

def  register(req):
     if req.method=='POST':
        name=req.POST['name']       
        email=req.POST['email']
        password=req.POST['password']
        send_mail('Lunessence registration', 'Welcome to Lunessence! Your account has been created successfully', settings.EMAIL_HOST_USER, [email])

        try:
            data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"user details already exits")
            return redirect(register)
     else:
         return render(req,'register.html')
     

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


# #------------------------------------- User--------------------------------------------------------------

def user_home(req):
    if 'user' in req.session:
        return render(req,'user/user_home.html')  
    else:
        return redirect(shop_login)
    
def destination_wedding(request):
        des = DestinationWedding.objects.all() 
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

def invitation_address_page(request, id):
    card = InvitationCard.objects.get(pk=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        order_date = request.POST.get('date')

        quantity = request.POST.get('qty_card', '1')  
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1  

        user_address = Address(user=request.user, name=name, address=address, phone_number=phone_number, email=email)
        user_address.save()

        price = card.price

        buy = BuyInv(
            user=request.user,
            inv=card,
            qty=quantity,  
            price=price,
            date=order_date,
            address=user_address
        )
        buy.save()

        return redirect('view_bookings')

    return render(request, 'user/order.html', {'card': card})


def des_address_page(req, id):
    des = DestinationWedding.objects.get(id=id)

    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')
        email = req.POST.get('email')
        wedding_date = req.POST.get('date')  

        user_address = Address(user=req.user, name=name, address=address, phone_number=phone_number, email=email)
        user_address.save()

        buy = BuyDesWedding(user=req.user, des=des, price=des.package_price, date=wedding_date, address=user_address)
        buy.save()

        return redirect(view_bookings)

    return render(req, 'user/order.html', {'des': des})

def items_address_page(request, item_ids):
    item_ids = item_ids.split(',')  
    items = Item.objects.select_related('category').filter(id__in=item_ids) 

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        order_date = request.POST.get('date')

        user_address = Address(user=request.user, name=name, address=address, phone_number=phone_number, email=email)
        user_address.save()

        for item in items:
            quantity = int(request.POST.get(f'qty_{item.id}', 1))  
            price = item.category.price  

            order = BuyItem(
                user=request.user, 
                item=item, 
                quantity=quantity,  
                price=price,  
                date=order_date, 
                address=user_address
            )
            order.save()

        return redirect('view_bookings')  

    return render(request, 'user/order.html', {'items': items})


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
