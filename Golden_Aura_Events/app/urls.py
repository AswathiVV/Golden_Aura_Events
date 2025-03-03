from django.urls import path
from . import views
urlpatterns=[
    path('',views.shop_login),
    path('register/',views.register),
    path('logout/',views.shop_logout),
    path('contact_us/', views.contact_us, name='contact_us'),
    # ___ shop _____________________________________________________________________________

    path('shop_home',views.shop_home),
    
    path("add_deswedding/", views.add_deswedding, name="add_deswedding"),
    path("add_category/",views.add_category, name="add_category"),
    path("add_item/",views.add_item, name="add_item"),
    path('add_invitation_category/',views.add_invitation_category, name='add_invitation_category'),
    path('add_invitation_card/',views.add_invitation_card, name='add_invitation_card'),


    path("shop_destination_weddings",views.shop_destination_weddings, name="shop_destination_weddings"),
    path("edit_wedding/<int:wedding_id>/", views.edit_wedding, name="edit_wedding"),
    path("delete-wedding/<int:wedding_id>/",views.delete_wedding, name="delete_wedding"), 
    path('add_categoryitem/<int:category_id>/', views.add_item, name='add_categoryitem'),  


    path('shop_items/', views.shop_items, name='shop_items'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path("shop_invitations/", views.shop_invitations, name="shop_invitations"),
    path("edit_invitation_category/<int:category_id>/", views.edit_invitation_category, name="edit_invitation_category"),
    path("delete_invitation_category/<int:category_id>/", views.delete_invitation_category, name="delete_invitation_category"),
    path("edit_invitation_card/<int:card_id>/", views.edit_invitation_card, name="edit_invitation_card"),
    path("delete_invitation_card/<int:card_id>/", views.delete_invitation_card, name="delete_invitation_card"),

    path('admin_bookings/',views.admin_bookings, name='admin_bookings'),

    path('cancel_order/<int:order_id>/<str:order_type>/',views.cancel_order, name='cancel_order'),
    path('confirm_order/<int:order_id>/<str:order_type>/',views.confirm_order, name='confirm_order'),

    # path('toggle_confirmation/<int:order_id>/<str:order_type>/',views.toggle_confirmation, name='toggle_confirmation'),

path('toggle_confirmation/<int:order_id>/<str:order_type>/', views.toggle_confirmation, name='toggle_confirmation'),


    # path('admin_bookings/', views.admin_bookings, name='admin_bookings'),
    # path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    # path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    # path('toggle_confirmation/<int:order_id>/', views.toggle_confirmation, name='toggle_confirmation'),

    #_____user______________________________________________________________________________

    path('user_home',views.user_home),
    path('about',views.about),
    path('contact',views.contact, name='contact'),

    path('invitation',views.invitation),
    path('invitation_detail/<id>',views.invitation_detail, name='invitation_detail'),

    path('destination_wedding',views.destination_wedding),
    path('view_des_wed/<id>',views.view_des_wed),
    path('buy_des/<int:id>/', views.buy_des, name='buy_des'), 
    # path('des_address_page/<int:id>/', views.des_address_page, name='des_address_page'),
    # path('invitation_address_page/<int:id>/', views.invitation_address_page, name='invitation_address_page'),
    # path('order/address/items/<str:item_ids>/', views.items_address_page, name='items_address_page'),
    # path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('item',views.item),
    path('buy_item/<int:id>/', views.buy_item, name='buy_item'), 
    # path('cancel-booking/<str:booking_type>/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),


    path('profile/', views.profile_view, name='profile_view'),
    path('add-address/', views.add_address, name='add_address'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('delete_account', views.delete_account, name='delete_account'),
    path('update_profile', views.update_profile, name='update_profile'),


    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('delete_order/<int:id>/', views.delete_order, name='delete_order'),


    # path('des-address/<int:id>/', views.des_address_page, name='des_address_page'),
    # path('items-address/<str:item_ids>/', views.items_address_page, name='items_address_page'),
    # path('invitation-address/<int:id>/', views.invitation_address_page, name='invitation_address_page'),
#     path('address/<str:type>/<int:id>/', views.address_page, name='address_page'),
# path('address/<str:type>/<path:ids>/', views.address_page, name='address_page_multiple'),

# path('address/<str:type>/<path:ids>/', views.address_page, name='address_page'),


    # path('order-payment/', views.order_payment, name='order_payment'),
    # path('pay/', views.pay, name='pay'),
    # # path('callback/', views.payment_callback, name='payment_callback'),
    # path("callback/",views.callback, name="payment_callback"),

    # path('view-bookings/', views.view_bookings, name='view_bookings'),
    path('des-address/<int:id>/', views.des_address_page, name='des_address_page'),
    path('inv-address/<int:id>/', views.invitation_address_page, name='invitation_address_page'),
    # path('items-address/<str:item_ids>/', views.items_address_page, name='items_address_page'),
path('order/address/items/<str:item_ids>/', views.items_address_page, name='items_address_page'),

    path('des-payment/', views.des_order_payment, name='des_order_payment'),
    path('inv-payment/', views.invitation_order_payment, name='invitation_order_payment'),
    path('items-payment/', views.items_order_payment, name='items_order_payment'),

    path('pay/', views.pay, name='pay'),

    path('bookings/', views.view_bookings, name='view_bookings'),
    path("callback/",views.callback, name="callback"),




]