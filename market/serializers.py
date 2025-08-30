from rest_framework import serializers
from .models import Product, Category
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Category, Product

from datetime import date


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']



class CategoryField(serializers.SlugRelatedField):
    """
    Custom field to allow lookup by slug OR name for category.
    """
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(slug=data)
        except Category.DoesNotExist:
            try:
                return self.get_queryset().get(name__iexact=data)
            except Category.DoesNotExist:
                self.fail('does_not_exist', slug_name=self.slug_field, value=data)



class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.CharField()  # Accept slug or name as input
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'harvest_date', 'price', 'description', 'category', 'stock']
        read_only_fields = ['slug']

    def validate_category(self, value):
        """
        Ensure category exists. Accept both slug or name.
        """
        try:
            return Category.objects.get(slug=value)
        except Category.DoesNotExist:
            try:
                return Category.objects.get(name__iexact=value)
            except Category.DoesNotExist:
                raise ValidationError(f"Category '{value}' does not exist. Please choose from available categories.")

    def create(self, validated_data):
        category_obj = validated_data.pop('category')
        validated_data['category'] = category_obj
        validated_data['farmer'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            category_obj = validated_data.pop('category')
            validated_data['category'] = category_obj
        # Prevent manual slug update
        if 'slug' in validated_data:
            validated_data.pop('slug')
        return super().update(instance, validated_data)


    def validate_harvest_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Harvest date cannot be in the future.")
        return value
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock(self, value):
        if value < 1:
            raise serializers.ValidationError("Stock must be at least 1.")
        return value
    
    
    def to_representation(self, instance):
        """
        Show category name and slug in response.
        """
        rep = super().to_representation(instance)
        rep['category'] = {
            'name': instance.category.name,
            'slug': instance.category.slug
        }
        return rep