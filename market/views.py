from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters, status, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.exceptions import PermissionDenied
from .permissions import IsFarmerOwner, IsFarmerOrReadOnly, IsFarmerOwner, IsFarmerUser
from rest_framework.response import Response
from rest_framework.decorators import action


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Categories.
    - Anyone can list/retrieve categories
    - Only admin can create/update/delete categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsFarmerOrReadOnly]

    # 🔍 Add search, filtering, ordering
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]

    # Fields allowed for search (partial match)
    search_fields = ["name", "category", "location"]

    # Fields allowed for exact filtering
    filterset_fields = ["category", "location"]

    # Allow ordering
    ordering_fields = ["price", "created_at"]

    def get_permissions(self):
        """
        - List/Retrieve → Anyone
        - Create → Authenticated farmers
        - Update/Delete → Owner farmer
        - my-products → Authenticated farmers only
        """
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), IsFarmerUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsFarmerOwner()]
        elif self.action == 'my_products':
            return [permissions.IsAuthenticated(), IsFarmerUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """
        Default: Return all active products for list and retrieve.
        """
        queryset = Product.objects.filter(is_active=True)

        # Optional filtering
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)

        owner = self.request.query_params.get('owner')
        if owner:
            queryset = queryset.filter(owner__id=owner)

        return queryset

    @action(detail=False, methods=['get'], url_path='my-products')
    def my_products(self, request):
        """
        Custom endpoint for farmers to view only their products.
        URL: /api/market/my-products/
        """
        products = Product.objects.filter(farmer=request.user, is_active=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-name/(?P<slug>[^/.]+)')
    def by_slug(self, request, slug=None):
        """
        Return all products that share the same slug (case-insensitive).
        """
        products = Product.objects.filter(slug__iexact=slug, is_active=True)
        if not products.exists():
            return Response({"detail": "No products found with this slug."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
