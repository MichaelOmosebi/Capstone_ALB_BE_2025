# market/tests/test_products.py
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from market.models import Category, Product
from rest_framework import status

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
    

    def test_retrieve_products_by_slug(self):
        """Should return all products that share the same slug"""
        self.client.login(username='farmer1', password='pass1234')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both farmer1 and farmer2's products
        self.assertEqual(response.data[0]['slug'], 'tomato')

    def test_by_slug_returns_multiple_products(self):
        url = reverse('product-by-slug', kwargs={'slug': 'fresh-tomatoes'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['slug'], 'fresh-tomatoes')

    def test_by_slug_not_found(self):
        url = reverse('product-by-slug', kwargs={'slug': 'non-existent'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'No products found with this slug.')

    def test_future_harvest_date_rejected(self):
        future_date = date.today() + timedelta(days=5)
        data = {
            "name": "Cabbage",
            "harvest_date": future_date,
            "price": "1200.00",
            "stock": 20,
            "description": "Fresh cabbage",
            "category": "vegetables"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('harvest_date', response.data)
        self.assertEqual(response.data['harvest_date'][0], "Harvest date cannot be in the future.")