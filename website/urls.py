from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('signup/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('fooder/', views.fooder, name='fooder'),
    path('order/', views.order, name='order'),
    path('orders/', views.orders, name='orders'),
    path('buy/', views.buy, name='buy'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('tile-shop/', views.tile_shop, name='tile_shop'),
    path('tile-shop/cart/', views.tile_cart, name='tile_cart'),
    path('tile-shop/cart/add/<int:tile_id>/', views.add_tile_to_cart, name='add_tile_to_cart'),
    path('tile-shop/cart/update/<int:tile_id>/', views.update_tile_cart, name='update_tile_cart'),
    path('tile-shop/cart/remove/<int:tile_id>/', views.remove_tile_from_cart, name='remove_tile_from_cart'),
    path('tile-shop/checkout/', views.tile_checkout, name='tile_checkout'),
]
