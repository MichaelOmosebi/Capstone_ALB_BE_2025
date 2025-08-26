from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "farmer", "price", "stock", "location", "created_at")
    list_filter = ("category", "location", "created_at")
    search_fields = ("name", "description")
    autocomplete_fields = ("farmer", "category")

