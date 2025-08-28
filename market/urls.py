from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    # Custom endpoint for searching products by slug
    path('products/<slug:slug>/', ProductViewSet.as_view({'get': 'by_slug'}), name='product-by-slug'),
]
