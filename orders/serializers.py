from rest_framework import serializers
from .models import Order, OrderItem
from wallet.models import Wallet
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    farmer_name = serializers.ReadOnlyField(source="product.farmer.username")

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "farmer_name", "quantity", "price"]
        extra_kwargs = {"price": {"read_only": True}}


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    buyer_name = serializers.ReadOnlyField(source="buyer.username")

    class Meta:
        model = Order
        fields = [
            "id", "buyer", "buyer_name", "status", "total_amount",
            "created_at", "updated_at", "items"
        ]
        read_only_fields = ["buyer", "total_amount", "status", "created_at", "updated_at"]

    def validate(self, data):
        user = self.context["request"].user
        for item in data["items"]:
            if item["product"].farmer == user:
                raise serializers.ValidationError("You cannot order your own product.")
            if item["quantity"] > item["product"].stock:
                raise serializers.ValidationError(f"Not enough stock for {item['product'].name}.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user
        order = Order.objects.create(buyer=user, **validated_data)

        total = 0
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]
            price = product.price

            # Reduce stock
            product.stock -= quantity
            product.save()

            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total += price * quantity

        # Wallet logic
        buyer_wallet, created = Wallet.objects.get_or_create(user=user)
        if buyer_wallet.balance < total:
            raise serializers.ValidationError("Insufficient wallet balance.")

        buyer_wallet.debit(total, description=f"Purchase Order #{order.id}")

        # Credit sellers
        for item_data in items_data:
            product = item_data["product"]
            seller_wallet = Wallet.objects.get(user=product.farmer)
            seller_wallet.credit(item_data["quantity"] * product.price, description=f"Sale Order #{order.id}")

        order.total_amount = total
        order.save()
        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        allowed_statuses = ['pending', 'processing', 'shipped', 'delivered', 'canceled']
        if value not in allowed_statuses:
            raise serializers.ValidationError("Invalid status.")
        return value

    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)
        if instance.status != 'canceled' and new_status == 'canceled':
            for item in instance.items.all():
                item.product.stock += item.quantity
                item.product.save()
        instance.status = new_status
        instance.save()
        return instance
