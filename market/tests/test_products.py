from rest_framework.test import APITestCase
from django.urls import reverse
from market.models import Product, CustomUser
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.farmer = CustomUser.objects.create_user(
            username="farmer1", password="password123", role="farmer"
        )
        self.retailer = CustomUser.objects.create_user(
            username="retailer1", password="password123", role="retailer"
        )
        self.product_url = reverse("product-list")

    def test_farmer_can_create_product_with_image(self):
        self.client.login(username="farmer1", password="password123")
        image = SimpleUploadedFile("tomatoes.jpg", b"file_content", content_type="image/jpeg")

        data = {
            "name": "Tomatoes",
            "category": "Vegetables",
            "location": "Lagos",
            "price": "250.00",
            "image": image,
        }
        response = self.client.post(self.product_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_retailer_cannot_create_product(self):
        self.client.login(username="retailer1", password="password123")
        data = {"name": "Pepper", "category": "Vegetables", "location": "Lagos", "price": "300.00"}
        response = self.client.post(self.product_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
