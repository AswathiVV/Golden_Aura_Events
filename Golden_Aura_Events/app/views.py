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


# def shop_items(req):
#     categories = ItemCategory.objects.all()
#     items = Item.objects.all()
#     return render(req, "shop/items.html", {"categories": categories, "items": items})

# def edit_category(req, category_id):
#     category = get_object_or_404(ItemCategory, pk=category_id)

#     if req.method == 'POST':
#         category.name = req.POST.get('name')
#         category.price = req.POST.get('price')
#         file = req.FILES.get('img')

#         if file:
#             category.img = file

#         category.save()
#         return redirect(shop_items)

#     return render(req, "shop/edit_item.html", {"category": category})

# def delete_category(req, category_id):
#     get_object_or_404(ItemCategory, pk=category_id).delete()
#     return redirect(shop_items)

# def edit_item(req, item_id):
#     item = get_object_or_404(Item, pk=item_id)

#     if req.method == 'POST':
#         item.name = req.POST.get('name')
#         file = req.FILES.get('img')

#         if file:
#             item.img = file

#         item.save()
#         return redirect(shop_items)

#     categories = ItemCategory.objects.all()
#     return render(req, "shop/edit_item.html", {"item": item, "categories": categories})



# def delete_item(req, item_id):
#     get_object_or_404(Item, pk=item_id).delete()
#     return redirect(shop_items)

def shop_items(req):
    categories = ItemCategory.objects.all()
    items = Item.objects.all()
    return render(req, "shop/items.html", {"categories": categories, "items": items})

# Edit Category
# def edit_category(req, category_id):
#     category = get_object_or_404(ItemCategory, pk=category_id)

#     if req.method == 'POST':
#         category.name = req.POST.get('name')
#         category.price = req.POST.get('price')
#         file = req.FILES.get('img')

#         if file:
#             category.img = file

#         category.save()
#         return redirect(shop_items)

#     return render(req, "shop/edit_item.html", {"category": category, "edit_type": "category"})

# Delete Category
def delete_category(req, category_id):
    get_object_or_404(ItemCategory, pk=category_id).delete()
    return redirect(shop_items)

# def edit_item(req, item_id):
#     item = get_object_or_404(Item, pk=item_id)

#     if req.method == 'POST':
#         item.name = req.POST.get('name')
#         file = req.FILES.get('img')

#         if file:
#             item.img = file

#         item.save()
#         return redirect(shop_items)

#     categories = ItemCategory.objects.all()
#     return render(req, "shop/edit_item.html", {"item": item, "categories": categories, "edit_type": "item"})

# Delete Item
def delete_item(req, item_id):
    get_object_or_404(Item, pk=item_id).delete()
    return redirect(shop_items)


def add_categoryitem(req, category_id):
    category = get_object_or_404(ItemCategory, pk=category_id)

    if req.method == 'POST':
        name = req.POST.get('name')
        file = req.FILES.get('img')

        if name and file:
            Item.objects.create(category=category, name=name, img=file)
            return redirect('shop_items')

    return render(req, "shop/add_item.html", {"category": category})

# def edit_item(req, item_id):
#     item = get_object_or_404(Item, pk=item_id)
#     categories = ItemCategory.objects.all() 

#     if req.method == 'POST':
#         item.name = req.POST.get('name')
#         file = req.FILES.get('img')
#         if file:
#             item.img = file
#         item.save()
#         return redirect(shop_items)

#     return render(req, "shop/edit_item.html", {"item": item, "categories": categories, "edit_type": "item"})

def edit_item(req, item_id):
    item = get_object_or_404(Item, pk=item_id)
    
    # Fetch category only if item belongs to one (adjust as per your DB structure)
    category = item.category if hasattr(item, 'category') else None 

    if req.method == 'POST':
        item.name = req.POST.get('name')
        file = req.FILES.get('img')

        if file:
            item.img = file

        item.save()
        return redirect(shop_items)

    categories = ItemCategory.objects.all()
    return render(req, "shop/edit_item.html", {
        "item": item,
        "category": category,  # Ensure category is passed
        "categories": categories,
        "edit_type": "item"
    })

# Edit Category
def edit_category(req, category_id):
    category = get_object_or_404(ItemCategory, pk=category_id)

    if req.method == 'POST':
        category.name = req.POST.get('category_name')  # ✅ Fixed field name
        category.price = req.POST.get('category_price')  # ✅ Fixed field name
        file = req.FILES.get('category_img')  # ✅ Fixed field name

        if file:
            category.img = file

        category.save()
        return redirect('shop_items')  # ✅ Fixed redirect

    categories = ItemCategory.objects.all()
    return render(req, "shop/edit_item.html", {"category": category, "categories": categories, "edit_type": "category"})


# #------------------------------------- User--------------------------------------------------------------

def user_home(req):
    if 'user' in req.session:
        return render(req,'user/user_home.html')  
    else:
        return redirect(shop_login)
    
def destination_wedding(request):
        weddings = DestinationWedding.objects.all() 
        return render(request, 'user/destination_wedding.html', {'weddings': weddings})
    
    
def view_des_wed(req,id):
     if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        weddings=DestinationWedding.objects.get(pk=id)
          
        return render(req,'user/des_wed_details.html',{'DestinationWedding':weddings}) 
     else:
         return redirect(shop_home)  
     
def wedding_planners(req):
    return render(req,'user/event_planners.html')
     
def photographers(req):
    return render(req,'user/photographers.html')

def beauty(req):
    return render(req,'user/beauty.html')




# def user_view_bookings(request):
#     if 'user' in request.session:
#         user = request.user
#         data = Buy.objects.filter(user=user).prefetch_related('buyitem_set__item__category').order_by('-purchase_date')
#         for booking in data:
#             booking.is_cancellable = (date.today() - booking.purchase_date) <= timedelta(days=2)

#             print("Booking ID:", booking.id)
#             print("Wedding:", booking.wedding)  
#             print("Invitation:", booking.invitation) 
            
#         return render(request, 'user/bookings.html', {'data': data})
#     else:
#         return redirect('login')

def user_view_bookings(request):
    if 'user' in request.session:
        user = request.user
        
        # Fetch the user's bookings and prefetch related data
        data = Buy.objects.filter(user=user).prefetch_related('buyitem_set__item__category').order_by('-purchase_date')
        
        # Loop through each booking and check if it's cancellable
        for booking in data:
            booking.is_cancellable = (date.today() - booking.purchase_date) <= timedelta(days=2)

            # Debugging: print booking details
            print("Booking ID:", booking.id)
            print("Wedding:", booking.wedding)  # Should not be None if wedding is assigned
            print("Invitation:", booking.invitation)  # Should not be None if invitation is assigned
            
            # Check if the wedding and invitation objects are properly linked
            if booking.wedding:
                print(f"Wedding exists: {booking.wedding.name}")
            else:
                print("No wedding linked to this booking.")
            
            if booking.invitation:
                print(f"Invitation exists: {booking.invitation.name}")
            else:
                print("No invitation linked to this booking.")
        
        return render(request, 'user/bookings.html', {'data': data})
    else:
        return redirect('login')


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Buy, id=booking_id, user=request.user)
    if booking.status == 'Pending' and (date.today() - booking.purchase_date).days <= 2:
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, "Booking has been canceled successfully.")
    else:
        messages.error(request, "Booking cannot be canceled.")
    return redirect('user_view_bookings')

# def item_category_list(req):
#     categories = ItemCategory.objects.all()
#     return render(req, 'user/categories.html', {'categories': categories})


from django.shortcuts import render, get_object_or_404
from .models import ItemCategory, Item

# View to display all categories
def category_list(request):
    categories = ItemCategory.objects.all()
    return render(request, 'user/category.html', {'categories': categories})

# View to display items in a specific category
def item_list(request, category_id):
    category = get_object_or_404(ItemCategory, pk=category_id)
    items = Item.objects.filter(category=category)
    return render(request, 'user/item.html', {'category': category, 'items': items})

# def contact_vendor(request, id=None, type=None): 
#     if request.method == "POST":
#         customer_name = request.POST.get("name")
#         customer_email = request.POST.get("email")
#         customer_phone = request.POST.get("phone")
#         message = request.POST.get("message", "")

#         wedding_id = request.POST.get("wedding_id")
#         invitation_id = request.POST.get("invitation_id")
#         item_ids = request.POST.getlist("item_ids")  

#         buy = Buy.objects.create(
#             user=request.user,
#             customer_name=customer_name,
#             customer_email=customer_email,
#             customer_phone=customer_phone,
#             message=message,
#             status="Pending",
#         )

#         if wedding_id:
#             buy.wedding = get_object_or_404(DestinationWedding, id=wedding_id)
#         if invitation_id:
#             buy.invitation = get_object_or_404(InvitationCard, id=invitation_id)

#         buy.save()

#         for item_id in item_ids:
#             item = get_object_or_404(Item, id=item_id)
#             BuyItem.objects.create(buy=buy, item=item, quantity=1)

#         return redirect("user_view_bookings")

#     items = Item.objects.all()
#     context = {"items": items}

#     if type == "wedding":
#         context["wedding"] = get_object_or_404(DestinationWedding, id=id)
#     elif type == "invitation":
#         context["invitation"] = get_object_or_404(InvitationCard, id=id)

#     return render(request, "user/contact_vendor.html", context)
def contact_vendor(request, id=None, type=None): 
    if request.method == "POST":
        # Get form data
        customer_name = request.POST.get("name")
        customer_email = request.POST.get("email")
        customer_phone = request.POST.get("phone")
        address = request.POST.get("address")

        wedding_id = request.POST.get("wedding_id")
        invitation_id = request.POST.get("invitation_id")
        item_ids = request.POST.getlist("item_ids")  

        # Create a Buy object
        buy = Buy.objects.create(
            user=request.user,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            address=address,
            status="Pending",
        )

        # If wedding ID is provided, link it to the Buy object
        if wedding_id:
            try:
                wedding = get_object_or_404(DestinationWedding, id=wedding_id)
                buy.wedding = wedding
            except DestinationWedding.DoesNotExist:
                # Handle the case where the wedding doesn't exist
                pass

        # If invitation ID is provided, link it to the Buy object
        if invitation_id:
            try:
                invitation = get_object_or_404(InvitationCard, id=invitation_id)
                buy.invitation = invitation
            except InvitationCard.DoesNotExist:
                # Handle the case where the invitation doesn't exist
                pass

        # Save the buy object after assigning wedding and invitation
        buy.save()

        # Create BuyItem objects for each item in the order
        for item_id in item_ids:
            item = get_object_or_404(Item, id=item_id)
            BuyItem.objects.create(buy=buy, item=item, quantity=1)

        return redirect("user_view_bookings")
    
    # Get items only if the type is correct (i.e., wedding or invitation)
    items = None
    if type == "items":
        items = Item.objects.all()  # Get items only if needed

    context = {"items": items}

    if type == "wedding":
        context["wedding"] = get_object_or_404(DestinationWedding, id=id)
    elif type == "invitation":
        context["invitation"] = get_object_or_404(InvitationCard, id=id)

    return render(request, "user/contact_vendor.html", context)




def item_category_list(request):
    categories = ItemCategory.objects.prefetch_related('item_set').all()
    item = Item.objects.all()
    return render(request, "user/categories.html", {"categories": categories, "item": item})

def invitation_list(request):
    categories = InvitationCategory.objects.all()
    invitation_cards = InvitationCard.objects.all()
    return render(request, 'user/invitation.html', {'categories': categories, 'invitation_cards': invitation_cards})


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Buy, id=booking_id)

    if booking.is_cancellable():
        booking.status = 'Cancelled'
        booking.save()
        return redirect("user_view_bookings")

    return redirect("user_view_bookings") 

