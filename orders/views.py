from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from rest_framework.exceptions import ValidationError

# ✅ Create new order
# Buyer-facing endpoints
class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(buyer=user)

# ✅ Order details (retrieve, update, delete by buyer)
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(buyer=user)

    def perform_update(self, serializer):
        # Prevent changing buyer or status here
        if 'status' in self.request.data:
            raise PermissionDenied("You cannot update order status here.")
        serializer.save()

# ✅ Cancel order (only buyer can cancel)
from rest_framework.views import APIView

class OrderCancelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.get(pk=pk, buyer=request.user)
        serializer = OrderSerializer()
        try:
            serializer.cancel_order(order)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Order canceled and stock restored."}, status=status.HTTP_200_OK)

# ✅ Admin/Staff update status
class OrderStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(buyer=user)
