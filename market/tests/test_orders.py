from rest_framework.test import APITestCase
from django.urls import reverse
from market.models import Product, Order, CustomUser
from rest_framework import status

class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.farmer = CustomUser.objects.create_user(
            username="farmer1", password="password123", role="farmer"
        )
        self.retailer = CustomUser.objects.create_user(
            username="retailer1", password="password123", role="retailer"
        )
        self.product = Product.objects.create(
            farmer=self.farmer,
            name="Tomatoes",
            category="Vegetables",
            location="Lagos",
            price=200,
        )
        self.order_url = reverse("order-list")

    def test_both_farmer_and_retailer_can_create_orders(self):
        # Farmer creates order
        self.client.login(username="farmer1", password="password123")
        response = self.client.post(self.order_url, {"product": self.product.id, "quantity": 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retailer creates order
        self.client.login(username="retailer1", password="password123")
        response = self.client.post(self.order_url, {"product": self.product.id, "quantity": 5})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_is_linked_to_user(self):
        self.client.login(username="retailer1", password="password123")
        response = self.client.post(self.order_url, {"product": self.product.id, "quantity": 3})
        self.assertEqual(Order.objects.first().user, self.retailer)
