from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import CustomUser as User
from market.models import Product, Order
from django.core.files.uploadedfile import SimpleUploadedFile

class MarketplaceAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.farmer = User.objects.create_user(email="farmer@test.com", password="pass1234", role="farmer")
        self.retailer = User.objects.create_user(email="retailer@test.com", password="pass1234", role="retailer")

        # Login farmer
        self.client.login(email="farmer@test.com", password="pass1234")

        # Create a product for testing
        self.product = Product.objects.create(
            name="Tomatoes",
            category="Vegetable",
            location="Lagos",
            price=100,
            farmer=self.farmer
        )

    # -------------------
    # PRODUCT TESTS
    # -------------------

    def test_farmer_can_create_product(self):
        url = reverse('product-list')
        data = {
            "name": "Onions",
            "category": "Vegetable",
            "location": "Kano",
            "price": 50
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retailer_cannot_create_product(self):
        self.client.logout()
        self.client.login(email="retailer@test.com", password="pass1234")
        url = reverse('product-list')
        data = {
            "name": "Carrots",
            "category": "Vegetable",
            "location": "Kaduna",
            "price": 70
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_farmer_can_update_product(self):
        url = reverse('product-detail', args=[self.product.id])
        data = {
            "name": "Updated Tomatoes",
            "category": "Vegetable",
            "location": "Lagos",
            "price": 150
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Tomatoes")

    def test_farmer_can_delete_product(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_farmer_can_upload_image_with_product(self):
        url = reverse('product-list')
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        data = {
            "name": "Pepper",
            "category": "Vegetable",
            "location": "Abuja",
            "price": 120,
            "image": image
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', response.data)

    # -------------------
    # ORDER TESTS
    # -------------------

    def test_retailer_can_create_order(self):
        self.client.logout()
        self.client.login(email="retailer@test.com", password="pass1234")
        url = reverse('order-list')
        data = {
            "product": self.product.id,
            "quantity": 3
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_farmer_cannot_create_order(self):
        url = reverse('order-list')
        data = {
            "product": self.product.id,
            "quantity": 5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retailer_can_view_orders(self):
        # First create an order
        self.client.logout()
        self.client.login(email="retailer@test.com", password="pass1234")
        Order.objects.create(product=self.product, retailer=self.retailer, quantity=2)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_retailer_can_delete_own_order(self):
        self.client.logout()
        self.client.login(email="retailer@test.com", password="pass1234")
        order = Order.objects.create(product=self.product, retailer=self.retailer, quantity=2)
        url = reverse('order-detail', args=[order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)






# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.urls import reverse
# from accounts.models import CustomUser
# from market.models import Product, Order, Category

# class MarketplaceAPITestCase(APITestCase):

#     def setUp(self):
#         # Users
#         self.farmer = CustomUser.objects.create_user(
#             username="farmer1",
#             email="farmer1@test.com",
#             password="farmerpass",
#             role=CustomUser.FARMER
#         )

#         self.retailer = CustomUser.objects.create_user(
#             username="retailer1",
#             email="retailer1@test.com",
#             password="retailerpass",
#             role=CustomUser.RETAILER
#         )

#         # Category
#         self.category = Category.objects.create(name="Vegetables")

#         # Product
#         self.product = Product.objects.create(
#             farmer=self.farmer,
#             name="Tomato",
#             description="Fresh tomatoes",
#             price=100.0,
#             stock=10,
#             location="Lagos",
#             category=self.category
#         )

#         # URLs
#         self.product_list_url = reverse("product-list")
#         self.order_url = reverse("order-list")

#     # ---------------- Product Tests ---------------- #

#     def test_farmer_can_create_product(self):
#         self.client.force_authenticate(user=self.farmer)
#         data = {
#             "name": "Carrot",
#             "description": "Fresh carrots",
#             "price": 50.0,
#             "stock": 15,
#             "location": "Abuja",
#             "category": self.category.id
#         }
#         response = self.client.post(self.product_list_url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Product.objects.count(), 2)

#     def test_retailer_cannot_create_product(self):
#         self.client.force_authenticate(user=self.retailer)
#         data = {
#             "name": "Carrot",
#             "description": "Fresh carrots",
#             "price": 50.0,
#             "stock": 15,
#             "location": "Abuja",
#             "category": self.category.id
#         }
#         response = self.client.post(self.product_list_url, data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_product_search_filter(self):
#         self.client.force_authenticate(user=self.farmer)
#         response = self.client.get(f"{self.product_list_url}?search=Tomato")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 1)

#     # ---------------- Order Tests ---------------- #

#     # def test_retailer_can_create_order(self):
#     #     self.client.force_authenticate(user=self.retailer)
#     #     data = {"product": self.product.id, "quantity": 3}
#     #     response = self.client.post(self.order_url, data)
#     #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     #     self.product.refresh_from_db()
#     #     self.assertEqual(self.product.stock, 7)
#     #     self.assertTrue(self.product.in_stock)
    
#     def test_retailer_can_create_order(self):
#         self.client.login(username="retailer1", password="testpass123")
#         response = self.client.post(
#             reverse("order-list"),
#             {"product": self.product.id, "quantity": 2},
#             format="json"
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_order_more_than_stock_fails(self):
#         self.client.force_authenticate(user=self.retailer)
#         data = {"product": self.product.id, "quantity": 20}
#         response = self.client.post(self.order_url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("Only", str(response.data))

#     # def test_farmer_cannot_create_order(self):
#     #     self.client.force_authenticate(user=self.farmer)
#     #     data = {"product": self.product.id, "quantity": 2}
#     #     response = self.client.post(self.order_url, data)
#     #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


#     def test_farmer_can_create_order(self):
#         self.client.login(username="farmer1", password="testpass123")
#         response = self.client.post(
#             reverse("order-list"),
#             {"product": self.product.id, "quantity": 1},
#             format="json"
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_in_stock_property_after_order(self):
#         self.client.force_authenticate(user=self.retailer)
#         # Order entire stock
#         data = {"product": self.product.id, "quantity": 10}
#         response = self.client.post(self.order_url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.product.refresh_from_db()
#         self.assertFalse(self.product.in_stock)
