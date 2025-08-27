from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsOrderOwner(BasePermission):
    """
    Only the user who created the order can update/delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.retailer == request.user
    


class IsFarmerOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.farmer == request.user



class IsFarmerOrRetailer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.role in ['farmer', 'retailer']
        )

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsFarmerOrReadOnly(BasePermission):
    """
    Only farmers who own the product can update/delete it.
    Everyone can read.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.farmer == request.user

class IsFarmerOwner(BasePermission):
    """
    Only the farmer who created the product can update/delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.farmer == request.user
    
class IsFarmerUser(BasePermission):
    """
    Allows access only to users with farmer role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'farmer'