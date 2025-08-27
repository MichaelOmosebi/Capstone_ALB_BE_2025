from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer, OrderStatusUpdateSerializer

# ✅ Create new order
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ List orders
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()  # Staff/Admin can see all
        return Order.objects.filter(buyer=user)  # Buyer sees only own orders

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

class OrderCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        user = request.user

        if order.buyer != user:
            raise PermissionDenied("You can only cancel your own order.")
        if order.status != "pending":
            return Response({"error": "Only pending orders can be canceled."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = "canceled"
        order.save()
        return Response({"message": "Order canceled successfully."}, status=status.HTTP_200_OK)

# ✅ Admin/Staff update status
class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
