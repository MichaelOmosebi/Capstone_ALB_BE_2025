from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from marketplace.models import Product, Order, OrderItem

User = get_user_model()

class OrderAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.buyer = User.objects.create_user(username="buyer", password="pass123")
        self.farmer = User.objects.create_user(username="farmer", password="pass123")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")

        # Create product for farmer
        self.product = Product.objects.create(
            name="Test Product",
            price=100,
            stock=10,
            farmer=self.farmer
        )

        # URLs
        self.list_url = reverse("order-list")
        self.create_url = reverse("order-create")

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def create_order(self):
        """Helper method to create an order for buyer"""
        payload = {
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 2
                }
            ]
        }
        response = self.client.post(self.create_url, payload, format="json")
        return response

    def test_buyer_can_create_order(self):
        self.authenticate(self.buyer)
        response = self.create_order()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.buyer, self.buyer)
        self.assertEqual(order.total_amount, 200)

    def test_buyer_cannot_order_own_product(self):
        self.authenticate(self.farmer)
        payload = {
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 1
                }
            ]
        }
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buyer_can_list_own_orders(self):
        self.authenticate(self.buyer)
        self.create_order()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_list_all_orders(self):
        self.authenticate(self.buyer)
        self.create_order()
        self.authenticate(self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_buyer_can_retrieve_own_order(self):
        self.authenticate(self.buyer)
        response = self.create_order()
        order_id = response.data["id"]
        detail_url = reverse("order-detail", kwargs={"pk": order_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], order_id)

    def test_buyer_cannot_view_others_order(self):
        self.authenticate(self.buyer)
        response = self.create_order()
        order_id = response.data["id"]

        other_user = User.objects.create_user(username="other", password="pass123")
        self.authenticate(other_user)
        detail_url = reverse("order-detail", kwargs={"pk": order_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_buyer_can_cancel_own_order(self):
        self.authenticate(self.buyer)
        response = self.create_order()
        order_id = response.data["id"]
        cancel_url = reverse("order-cancel", kwargs={"pk": order_id})
        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(pk=order_id).status, "canceled")

    def test_buyer_cannot_cancel_after_status_changes(self):
        self.authenticate(self.buyer)
        response = self.create_order()
        order_id = response.data["id"]

        # Change status to processing
        order = Order.objects.get(pk=order_id)
        order.status = "processing"
        order.save()

        cancel_url = reverse("order-cancel", kwargs={"pk": order_id})
        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_can_update_status(self):
        self.authenticate(self.buyer)
        response = self.create_order()
        order_id = response.data["id"]

        self.authenticate(self.admin)
        status_url = reverse("order-status-update", kwargs={"pk": order_id})
        payload = {"status": "processing"}
        response = self.client.patch(status_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(pk=order_id).status, "processing")

    def test_non_admin_cannot_update_status(self):
        self.authenticate(self.buyer)
        response = self.create_order()
        order_id = response.data["id"]

        status_url = reverse("order-status-update", kwargs={"pk": order_id})
        payload = {"status": "processing"}
        response = self.client.patch(status_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
