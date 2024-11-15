from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import Gafas, Wishlist, Cart
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Order
from .forms import RegisterForm
from django.conf import settings
from .services import PDFGenerator

from .serializer import TaskSerializer
from rest_framework import viewsets

class ApiproductsView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Gafas.objects.all()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('gafas_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('gafas_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@login_required
def gafas_list(request):
    gafas = Gafas.objects.all()
    return render(request, 'accounts/gafas_list.html', {'gafas': gafas})

@login_required
def add_to_wishlist(request, gafa_id):
    gafa = get_object_or_404(Gafas, id=gafa_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.gafas.add(gafa)
    messages.success(request, 'Añadido a la wishlist con éxito')
    return redirect('gafas_list')

@login_required
def add_to_cart(request, gafa_id):
    gafa = get_object_or_404(Gafas, id=gafa_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.gafas.add(gafa)
    messages.success(request, 'Añadido al carrito con éxito')
    return redirect('gafas_list')

@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    gafas = wishlist.gafas.all()
    return render(request, 'accounts/wishlist.html', {'gafas': gafas})

@login_required
def remove_from_wishlist(request, gafa_id):
    gafa = get_object_or_404(Gafas, id=gafa_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.gafas.remove(gafa)
    messages.success(request, 'Eliminado de la wishlist con éxito')
    return redirect('wishlist')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    gafas = cart.gafas.all()
    total_price = cart.total_price()
    return render(request, 'accounts/cart.html', {'gafas': gafas, 'total_price': total_price})

@login_required
def remove_from_cart(request, gafa_id):
    gafa = get_object_or_404(Gafas, id=gafa_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart.gafas.remove(gafa)
    messages.success(request, 'Eliminado del carrito con éxito')
    return redirect('cart')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = cart.total_price()
    weather_data = get_weather()
    weather_description = weather_data['weather'][0]['description']
    
    if 'rain' in weather_description:
        estimated_delivery = '3-4 días'
    elif 'clear' in weather_description:
        estimated_delivery = '1-2 días'
    else:
        estimated_delivery = '2-3 días'

    if request.method == 'POST':
        address = request.POST['address']
        payment_method = request.POST['payment_method']
        order = Order.objects.create(user=request.user, address=address, payment_method=payment_method)
        order.gafas.set(cart.gafas.all())
        cart.gafas.clear()
        return redirect('profile')
    
    return render(request, 'accounts/checkout.html', {
        'cart': cart,
        'total_price': total_price,
        'estimated_delivery': estimated_delivery
    })


@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'accounts/order_summary.html', {'order': order})

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'accounts/profile.html', {'user': user, 'orders': orders})

@login_required
def gafas_list(request):
    gafas = Gafas.objects.all()

    # Filtros
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_stock = request.GET.get('min_stock')
    max_stock = request.GET.get('max_stock')
    order_by = request.GET.get('order_by')

    if min_price:
        gafas = gafas.filter(precio__gte=min_price)
    if max_price:
        gafas = gafas.filter(precio__lte=max_price)
    if min_stock:
        gafas = gafas.filter(stock__gte=min_stock)
    if max_stock:
        gafas = gafas.filter(stock__lte=max_stock)

    # Ordenación
    if order_by:
        gafas = gafas.order_by(order_by)

    return render(request, 'accounts/gafas_list.html', {'gafas': gafas})



#API WEATHER

def get_weather():
    api_key = settings.OPENWEATHERMAP_API_KEY
    city = 'Medellin'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


@login_required
def download_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    weather_data = get_weather()
    weather_description = weather_data['weather'][0]['description']
    
    if 'rain' in weather_description:
        estimated_delivery = '3-4 días'
    elif 'clear' in weather_description:
        estimated_delivery = '1-2 días'
    else:
        estimated_delivery = '2-3 días'

    pdf_generator = PDFGenerator()
    pdf_buffer = pdf_generator.generate_order_pdf(order, estimated_delivery)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.id}.pdf"'
    return response


@login_required
def send_order_pdf_email(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    weather_data = get_weather()
    weather_description = weather_data['weather'][0]['description']
    
    if 'rain' in weather_description:
        estimated_delivery = '3-4 días'
    elif 'clear' in weather_description:
        estimated_delivery = '1-2 días'
    else:
        estimated_delivery = '2-3 días'

    pdf_generator = PDFGenerator()
    pdf_generator.send_order_pdf_email(order, estimated_delivery)

    messages.success(request, 'El PDF del pedido ha sido enviado a tu correo electrónico.')
    return redirect('profile')