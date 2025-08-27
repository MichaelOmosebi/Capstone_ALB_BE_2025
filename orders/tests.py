from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from market.models import Product, Category
from .models import Order

User = get_user_model()

class OrderTestCase(APITestCase):
    def setUp(self):
        self.farmer = User.objects.create_user(username='farmer1', password='pass1234', role='farmer')
        self.retailer = User.objects.create_user(username='retailer1', password='pass1234', role='retailer')
        self.category = Category.objects.create(name='Fruits')
        self.product = Product.objects.create(farmer=self.farmer, name='Mango', price=50, stock=10, category=self.category)
        self.token = Token.objects.create(user=self.retailer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_retailer_can_place_order(self):
        url = reverse('order-list')
        data = {
            "items": [
                {"product": self.product.id, "quantity": 2, "price": 50}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
