from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from market.models import Product, Category
from orders.models import Order, OrderItem

User = get_user_model()

class OrderAPITestCase(APITestCase):
    def setUp(self):
        # Users
        self.farmer = User.objects.create_user(
            username="farmer", password="pass123", role="farmer"
        )
        self.retailer = User.objects.create_user(
            username="retailer", password="pass123", role="retailer"
        )
        self.admin = User.objects.create_superuser(
            username="admin", password="adminpass"
        )

        # Category
        self.category = Category.objects.create(name="Vegetables")

        # Product by farmer
        self.product = Product.objects.create(
            name="Tomato",
            price=100,
            stock=10,
            farmer=self.farmer,
            location="Farm A",
            category=self.category
        )

        # URLs
        self.list_url = reverse("order-list-create")

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def create_order(self, user, product, quantity=1):
        """Helper method to create an order"""
        self.authenticate(user)
        payload = {"items": [{"product": product.id, "quantity": quantity}]}
        return self.client.post(self.list_url, payload, format="json")

    def test_farmer_can_create_order_for_other_farmer_product(self):
        """Farmer cannot order own product, but can order others"""
        # Attempt ordering own product
        response = self.create_order(self.farmer, self.product)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create another farmer and product
        other_farmer = User.objects.create_user(username="farmer2", password="pass123", role="farmer")
        other_product = Product.objects.create(
            name="Cabbage", price=50, stock=20, farmer=other_farmer, location="Farm B", category=self.category
        )
        response = self.create_order(self.farmer, other_product, quantity=5)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retailer_can_create_order(self):
        response = self.create_order(self.retailer, self.product, quantity=2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)  # Stock reduced

    def test_buyer_can_list_own_orders_only(self):
        self.create_order(self.retailer, self.product)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only the authenticated user's orders are returned
        self.assertTrue(all(order['buyer'] == self.retailer.id for order in response.data))

    def test_admin_can_list_all_orders(self):
        self.create_order(self.retailer, self.product)
        self.authenticate(self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_order_cancellation_restores_stock(self):
        response = self.create_order(self.retailer, self.product, quantity=2)
        order_id = response.data['id']
        cancel_url = reverse("order-cancel", kwargs={"pk": order_id})

        # Buyer cancels order
        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)  # Stock restored

    def test_only_buyer_can_cancel_order(self):
        response = self.create_order(self.retailer, self.product, quantity=2)
        order_id = response.data['id']

        self.authenticate(self.farmer)  # Another user
        cancel_url = reverse("order-cancel", kwargs={"pk": order_id})
        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_update_status(self):
        response = self.create_order(self.retailer, self.product, quantity=1)
        order_id = response.data['id']

        self.authenticate(self.admin)
        status_url = reverse("order-status-update", kwargs={"pk": order_id})
        response = self.client.patch(status_url, {"status": "processing"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(pk=order_id).status, "processing")

    def test_non_admin_cannot_update_status(self):
        response = self.create_order(self.retailer, self.product)
        order_id = response.data['id']

        self.authenticate(self.retailer)
        status_url = reverse("order-status-update", kwargs={"pk": order_id})
        response = self.client.patch(status_url, {"status": "processing"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
