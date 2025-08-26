from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.exceptions import PermissionDenied

class IsFarmerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.farmer == request.user

class IsFarmerOrRetailer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.role in ['farmer', 'retailer']
        )

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsFarmerOwner

class ProductViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Products.
    - Farmers can create products
    - Anyone can list/search/filter products
    - Only the farmer-owner can update/delete their own product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # 🔍 Add search, filtering, ordering
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]

    # Fields allowed for search (partial match)
    search_fields = ["name", "category", "location"]

    # Fields allowed for exact filtering
    filterset_fields = ["category", "location"]

    # Allow ordering
    ordering_fields = ["price", "created_at"]

    def perform_create(self, serializer):
        """
        Only allow farmers to create products.
        If the logged-in user is not a farmer, raise a permission error.
        """
        if self.request.user.role != "farmer":
            raise PermissionDenied("Only farmers can create products.")

        # ✅ Save with logged-in farmer as owner
        serializer.save(farmer=self.request.user)

    def get_permissions(self):
        """
        - Update/Delete → Only farmer-owner
        - Create → Only authenticated farmers
        - List/Retrieve → Anyone
        """
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsFarmerOwner()]
        elif self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]




# class OrderCreateView(generics.CreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated, IsFarmerOrRetailer]

#     def perform_create(self, serializer):
#         serializer.save(retailer=self.request.user)
#         # Decrement product stock
#         product = serializer.validated_data['product']
#         product.stock -= serializer.validated_data['quantity']
#         product.save()


class IsOrderOwner(permissions.BasePermission):
    """
    Only the user who created the order can update/delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.retailer == request.user

class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET -> List all orders (auth required)
    POST -> Create a new order (Farmer or Retailer)
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 🔍 Enable search, filtering, and ordering
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    # Searchable fields
    search_fields = ["product__name", "buyer__username"]
    # Filterable fields
    filterset_fields = ["status", "product"]
    # Allow ordering
    ordering_fields = ["created_at", "quantity"]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the buyer
        serializer.save(buyer=self.request.user)

        # 🚫 Prevent farmers from ordering their own product
        if self.request.user == product.farmer:
            raise PermissionDenied("You cannot order your own product.")
        
        # Decrement product stock
        product = serializer.validated_data['product']
        product.stock -= serializer.validated_data['quantity']
        product.save()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET -> Retrieve a single order
    PUT/PATCH -> Update an order (only if user is owner)
    DELETE -> Cancel an order (only if user is owner)
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated(), IsOrderOwner()]
        return [permissions.IsAuthenticated()]
