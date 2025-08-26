from rest_framework import serializers
from .models import Product, Order
from rest_framework.exceptions import PermissionDenied

class ProductSerializer(serializers.ModelSerializer):
    in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'farmer', 'name', 'description', 'price', 'stock', 'location', 'category', 'image', 'in_stock', 'created_at', 'updated_at']
        read_only_fields = ['farmer', 'created_at', 'updated_at']


    def create(self, validated_data):
        user = self.context["request"].user
        if user.role != "farmer":
            raise PermissionDenied("Only farmers can create products.")
        validated_data["farmer"] = user
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    retailer = serializers.ReadOnlyField(source='retailer.username')
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Order
        fields = ['id', 'retailer', 'product', 'product_name', 'quantity', 'created_at']
        read_only_fields = ['retailer', 'product_name']

    def validate_quantity(self, value):
        product = self.initial_data.get('product')
        try:
            product_obj = Product.objects.get(pk=product)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")
        if value > product_obj.stock:
            raise serializers.ValidationError(f"Only {product_obj.stock} items available in stock")
        return value