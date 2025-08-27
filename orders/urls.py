from django.urls import path
from .views import (
    OrderListCreateAPIView,
    OrderDetailView,
    OrderCancelAPIView,
    OrderStatusUpdateAPIView
)

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/cancel/', OrderCancelAPIView.as_view(), name='order-cancel'),
    path('orders/<int:pk>/status/', OrderStatusUpdateAPIView.as_view(), name='order-status-update'),
]
