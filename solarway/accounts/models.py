from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

class Gafas(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='gafas/')

    def __str__(self):
        return self.nombre
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gafas = models.ManyToManyField(Gafas)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gafas = models.ManyToManyField(Gafas)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    def total_price(self):
        return sum(gafa.precio for gafa in self.gafas.all())
    
class Order(models.Model):
    
    STATUS_CHOICES = [
        ('cancelado', 'Cancelado'),
        ('en_proceso', 'En Proceso'),
        ('enviado', 'Enviado'),
        ('completado', 'Completado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gafas = models.ManyToManyField(Gafas)
    address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_proceso')


    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def total_price(self):
        return sum(gafa.precio for gafa in self.gafas.all())