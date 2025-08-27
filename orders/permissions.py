from rest_framework.permissions import BasePermission

class IsBuyerOrFarmerForOrder(BasePermission):
    """
    Allow buyer to update/cancel their order.
    Allow farmer to update the status if they own any product in the order.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == obj.buyer:
            return True
        # If farmer owns any product in the order items
        if user.role == "farmer" and obj.items.filter(product__farmer=user).exists():
            return True
        return False
