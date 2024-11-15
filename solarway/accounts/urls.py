from django.urls import path
from django.conf.urls import include
from . import views
from .views import home, gafas_list, wishlist, cart
from rest_framework import routers

router=routers.DefaultRouter()
router.register(r'products',views.ApiproductsView,'products')


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
    path('download_order_pdf/<int:order_id>/', views.download_order_pdf, name='download_order_pdf'),
    path('send_order_pdf_email/<int:order_id>/', views.send_order_pdf_email, name='send_order_pdf_email'),
    path('', home, name='home'),
    path('api/v1',include(router.urls)),
]