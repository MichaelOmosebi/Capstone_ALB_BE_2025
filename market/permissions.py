from rest_framework import permissions

class IsOrderOwner(permissions.BasePermission):
    """
    Only the user who created the order can update/delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.retailer == request.user
    


class IsFarmerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.farmer == request.user



class IsFarmerOrRetailer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.role in ['farmer', 'retailer']
        )
