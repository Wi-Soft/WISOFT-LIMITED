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
]
