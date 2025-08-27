from rest_framework import serializers
from .models import Order, OrderItem
from market.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if product.stock < quantity:
            raise serializers.ValidationError(f"Not enough stock for {product.name}")
        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['buyer', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        buyer = self.context['request'].user

        # Create the order
        order = Order.objects.create(buyer=buyer)

        # Create order items
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price  # Capture price at order time

            # Reduce stock
            product.stock -= quantity
            product.save()

            # Create order item
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

        return order
