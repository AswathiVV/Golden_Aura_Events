from django.urls import path
from . import views
urlpatterns=[
    path('user_home',views.user_home),
    path('shop_home',views.shop_home),
# ===============================================
    path("add_deswedding/", views.add_deswedding, name="add_deswedding"),

    path("add_category/",views.add_category, name="add_category"),
    path("add_item/",views.add_item, name="add_item"),
    path('add_invitation_category/',views.add_invitation_category, name='add_invitation_category'),
    path('add_invitation_card/',views.add_invitation_card, name='add_invitation_card'),


    path("shop_destination_weddings",views.shop_destination_weddings, name="shop_destination_weddings"),
    # path("edit_wedding/<int:wedding_id>/",views.edit_wedding, name="edit_wedding"),  
    path("edit_wedding/<int:wedding_id>/", views.edit_wedding, name="edit_wedding"),
    path("delete-wedding/<int:wedding_id>/",views.delete_wedding, name="delete_wedding"), 


    path('shop_items/', views.shop_items, name='shop_items'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),  # ✅ Fixed path
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('add_categoryitem/<int:category_id>/', views.add_item, name='add_categoryitem'),  # ✅ Fixes the issue


# ===============================================

    path('register',views.register),
    path('',views.shop_login),
    path('logout',views.shop_logout),

    path('destination_wedding',views.destination_wedding),
    # path('item_category_list',views.item_category_list),
    path('invitation_list',views.invitation_list),
    path('invitation_detail/<int:id>/',views.invitation_detail, name='invitation_detail'),
    path('customize/<int:id>/',views.customize_invitation, name='customize_invitation'),


    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('view_des_wed/<id>',views.view_des_wed),   
      
    path('contact_vendor/', views.contact_vendor, name='contact_vendor'),  
    path('contact_vendor/<int:id>/', views.contact_vendor, name='contact_vendor'),  
    path('contact_vendor/<int:id>/<str:type>/', views.contact_vendor, name='contact_vendor'),  

    path('wedding_planners',views.wedding_planners),
    path('photographers',views.photographers),
    path('beauty',views.beauty),
    
    # path('category_list', views.category_list, name='category_list'),
    # path('category/<int:category_id>/', views.item_list, name='item_list'),

    path('view_bookings/', views.user_view_bookings, name='user_view_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    # path('booking/<int:booking_id>/',views.user_booking_details, name='user_booking_details'),



    path('categories/',views.categories, name='categories'),
    path('categories/<int:category_id>/items/',views.items, name='items'),
    path('buy_item/', views.buy_item, name='buy_item'),

    path('contact_vendor/',views.contact_vendor, name='contact_vendor'), 
]