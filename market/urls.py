from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderDetailView, OrderListCreateView, ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path("orders/", OrderListCreateView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
