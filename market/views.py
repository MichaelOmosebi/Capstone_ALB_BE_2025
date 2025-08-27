from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.exceptions import PermissionDenied


from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from .models import Product, Category
from .serializers import ProductSerializer
from .permissions import IsFarmerOwner, IsFarmerOrRetailer, IsOrderOwner, ReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Categories.
    - Anyone can list/retrieve categories
    - Only admin can create/update/delete categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser | ReadOnly]

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
