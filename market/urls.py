from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    # Custom endpoint for searching products by slug
    path('products/by-name/<slug:slug>/', ProductViewSet.as_view({'get': 'by_slug'}), name='product-by-slug'),
    # Custom endpoint for searching Farmer’s own products
    path('products/my-products/', ProductViewSet.as_view({'get': 'my_products'}), name='my-products'),
]

# List all products
# ---GET /api/market/products/

# Retrieve single product by ID
# --- GET /api/market/products/<id>/

# Create product (farmer only)
# --- POST /api/market/products/

# Update/Delete product (owner farmer only)
# --- PUT/PATCH/DELETE /api/market/products/<id>/

# Farmer’s own products
# --- GET /api/market/products/my-products/

# Get products by name (slug)
# --- GET /api/market/products/by-name/<slug>/