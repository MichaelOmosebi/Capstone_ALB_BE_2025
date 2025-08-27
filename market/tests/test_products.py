# market/tests/test_products.py
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from market.models import Category, Product

User = get_user_model()

class ProductAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.farmer = User.objects.create_user(
            email="farmer@example.com",
            password="password123",
            role="farmer"
        )
        self.retailer = User.objects.create_user(
            email="retailer@example.com",
            password="password123",
            role="retailer"
        )
        self.category = Category.objects.create(name="Fruits")
        self.product = Product.objects.create(
            farmer=self.farmer,
            name="Tomatoes",
            description="Fresh tomatoes",
            price=500,
            stock=10,
            location="Lagos",
            category=self.category
        )

    def test_list_products(self):
        url = reverse('product-list')  # matches your router name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_product_only_farmer(self):
        url = reverse('product-list')
        data = {
            "name": "Onions",
            "description": "Organic onions",
            "price": 1000,
            "stock": 20,
            "location": "Abuja",
            "category": self.category.id
        }
        # Try as retailer → should fail
        self.client.force_authenticate(user=self.retailer)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

        # Try as farmer → should succeed
        self.client.force_authenticate(user=self.farmer)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "Onions")