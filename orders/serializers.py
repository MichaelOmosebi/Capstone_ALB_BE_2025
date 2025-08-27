from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    farmer_name = serializers.ReadOnlyField(source="product.farmer.name")

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "farmer_name", "quantity", "price"]
        extra_kwargs = {
            "price": {"read_only": True}
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    buyer_name = serializers.ReadOnlyField(source="buyer.name")

    class Meta:
        model = Order
        fields = [
            "id",
            "buyer",
            "buyer_name",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
            "items"
        ]
        # Status is still read-only here because updates happen via dedicated endpoint
        read_only_fields = ["buyer", "total_amount", "status", "created_at", "updated_at"]

    def validate(self, data):
        user = self.context["request"].user
        for item in data["items"]:
            if item["product"].farmer == user:
                raise serializers.ValidationError("You cannot order your own product.")
        return data

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user
        order = Order.objects.create(buyer=user, **validated_data)

        total = 0
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]
            price = product.price
            if quantity > product.stock:
                raise serializers.ValidationError(f"Not enough stock for {product.name}.")
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total += price * quantity
            # Reduce stock
            product.stock -= quantity
            product.save()

        order.total_amount = total
        order.save()
        return order


# ✅ Additional serializer for updating order status (used by staff/admin)
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
