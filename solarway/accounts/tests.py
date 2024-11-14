from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Gafas, Cart, Order

class AddToCartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.gafa = Gafas.objects.create(nombre='Test Gafa', descripcion='Test Description', precio=100, stock=10)

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('add_to_cart', args=[self.gafa.id]))
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        self.assertIn(self.gafa, cart.gafas.all())
        
        
class CreateOrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.gafa = Gafas.objects.create(nombre='Test Gafa', descripcion='Test Description', precio=100, stock=10)
        self.cart = Cart.objects.create(user=self.user)
        self.cart.gafas.add(self.gafa)

    def test_create_order(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('checkout'), {
            'address': 'Test Address',
            'payment_method': 'credit_card'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        order = Order.objects.get(user=self.user)
        self.assertIn(self.gafa, order.gafas.all())
        self.assertEqual(order.address, 'Test Address')
        self.assertEqual(order.payment_method, 'credit_card')
        

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')

    def test_login_page_access(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('gafas_list'))