from django.urls import path
from . import views
urlpatterns=[
    path('',views.shop_login),
    path('register',views.register),
    path('logout',views.shop_logout),

    # ___ shop _____________________________________________________________________________

    path('shop_home',views.shop_home),

    #_____user______________________________________________________________________________

    path('user_home',views.user_home),
    path('invitation',views.invitation),
    path('invitation_detail/<id>',views.invitation_detail, name='invitation_detail'),

    path('destination_wedding',views.destination_wedding),
    path('view_des_wed/<id>',views.view_des_wed),
    path('buy_des/<int:id>/', views.buy_des, name='buy_des'), 
    path('address_page/<int:id>/', views.address_page, name='address_page'),
    path('invitation_address_page/<int:id>/', views.invitation_address_page, name='invitation_address_page'),

    path('view_bookings/', views.view_bookings, name='view_bookings'),


]