from django.urls import path
from . import views
from .views import home, gafas_list, wishlist, cart


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('gafas/', gafas_list, name='gafas_list'),
    path('wishlist/', wishlist, name='wishlist'),
    path('cart/', cart, name='cart'),
    path('add_to_wishlist/<int:gafa_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add_to_cart/<int:gafa_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_wishlist/<int:gafa_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('remove_from_cart/<int:gafa_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('profile/', views.profile, name='profile'),
    path('', home, name='home'),
]