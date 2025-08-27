from rest_framework import serializers
from .models import Product, Category
from rest_framework.exceptions import PermissionDenied


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    farmer = serializers.ReadOnlyField(source='farmer.username')
    in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'farmer', 'name', 'description', 'category', 'price', 
                  'stock', 'in_stock', 'location', 'image', 'created_at']


# class ProductSerializer(serializers.ModelSerializer):
#     in_stock = serializers.ReadOnlyField()

#     class Meta:
#         model = Product
#         fields = ['id', 'farmer', 'name', 'description', 'price', 'stock', 'location', 'category', 'image', 'in_stock', 'created_at', 'updated_at']
#         read_only_fields = ['farmer', 'created_at', 'updated_at']


    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     if user.role != "farmer":
    #         raise PermissionDenied("Only farmers can create products.")
    #     validated_data["farmer"] = user
    #     return super().create(validated_data)
    

from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    farmer = serializers.ReadOnlyField(source='farmer.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'discount_price',
            'stock', 'unit', 'location', 'category', 'category_name',
            'image', 'tags', 'is_active', 'in_stock', 'farmer',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'in_stock', 'farmer']
