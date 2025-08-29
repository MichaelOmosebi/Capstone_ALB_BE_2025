from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Order
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from wallet.models import Wallet

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(buyer=user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=["get"], url_path="my-orders")
    def my_orders(self, request):
        orders = Order.objects.filter(buyer=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="cancel")
    @transaction.atomic
    def cancel_order(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk, buyer=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status != "pending":
            return Response({"detail": "Only pending orders can be canceled."}, status=status.HTTP_400_BAD_REQUEST)

        # Restore stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        # Refund buyer
        buyer_wallet = Wallet.objects.get(user=request.user)
        buyer_wallet.credit(order.total_amount, description=f"Refund for Order #{order.id}")

        order.status = "canceled"
        order.save()
        return Response({"detail": "Order canceled and stock restored."})
