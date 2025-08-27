from rest_framework import serializers
from .models import Order, OrderItem, Product

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
        fields = ["id", "buyer", "buyer_name", "status", "total_amount", "created_at", "updated_at", "items"]
        read_only_fields = ["buyer", "total_amount", "status", "created_at", "updated_at"]

    def validate(self, data):
        user = self.context["request"].user
        for item in data["items"]:
            if item["product"].farmer == user:
                raise serializers.ValidationError("You cannot order your own product.")
            if item["quantity"] > item["product"].stock:
                raise serializers.ValidationError(f"Not enough stock for {item['product'].name}.")
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

            # Reduce stock
            product.stock -= quantity
            product.save()

            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total += price * quantity

        order.total_amount = total
        order.save()
        return order

    def cancel_order(self, order):
        """Restore stock when order is canceled"""
        if order.status != "pending":
            raise serializers.ValidationError("Only pending orders can be canceled.")
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        order.status = "canceled"
        order.save()
        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        read_only_fields = []

    def validate_status(self, value):
        """Optional: Restrict which status values can be set"""
        allowed_statuses = ['pending', 'processing', 'shipped', 'delivered', 'canceled']
        if value not in allowed_statuses:
            raise serializers.ValidationError("Invalid status.")
        return value

    def update(self, instance, validated_data):
        """Handle side effects for specific status changes"""
        new_status = validated_data.get('status', instance.status)
        
        # Example: restore stock if order is canceled
        if instance.status != 'canceled' and new_status == 'canceled':
            for item in instance.items.all():
                item.product.stock += item.quantity
                item.product.save()
        
        instance.status = new_status
        instance.save()
        return instance
