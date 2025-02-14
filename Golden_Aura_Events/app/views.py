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

def categories(request):
    categories = ItemCategory.objects.all()
    return render(request, 'user/item_categories.html', {'categories': categories})

def items(request, category_id):
    category = get_object_or_404(ItemCategory, id=category_id)
    items = Item.objects.filter(category=category)
    return render(request, 'user/item.html', {'category': category, 'items': items})

# def buy_des(req,id):
#     des=DestinationWedding.objects.get(pk=id)
#     return redirect(address_page, id=id)

def buy_des(req, id):
    des = get_object_or_404(DeprecationWarning, pk=id)  
    return redirect(address_page, id=id)


def address_page(req, id):
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

    

def view_bookings(req):
    user = User.objects.get(username=req.session['user'])
    bookings = BuyDesWedding.objects.filter(user=user)[::-1]
    return render(req, 'user/view_bookings.html', {'bookings': bookings})
