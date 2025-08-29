from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]

# POST	/api/orders/	Create new order
# GET	/api/orders/	List all user’s orders
# GET	/api/orders/my-orders/	Get logged-in user orders
# POST	/api/orders/{id}/cancel/	Cancel an order
# PATCH	/api/orders/{id}/	Update status (admin only)