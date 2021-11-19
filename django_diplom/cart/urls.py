from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('addcart/<slug:product_slug>/', views.add_to_cart, name='add_to_cart'),
    path('addcart_addon/<slug:addon_slug>/', views.add_to_cart_addon, name='add_to_cart_addon'),

    path('showcart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
   path('makeorder/', views.MakeOrder, name='make_order'),

    path('addcart/removeproduct/<slug:product_slug>/', views.remove_product, name='remove_product'),
    path('addcart/change_quantity/<slug:product_slug>/', views.change_quantity, name='change_quantity'),
path('addcart_addon/removeproduct/<slug:addon_slug>/', views.remove_addon, name='remove_addon'),
    path('addcart_addon/change_quantity/<slug:addon_slug>/', views.change_quantity_addon, name='change_quantity_addon'),

]
