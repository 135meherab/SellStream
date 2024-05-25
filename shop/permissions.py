from rest_framework.permissions import BasePermission

    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is admin
        if request.user.is_staff:
            return True
        # Otherwise, only allow access if the owner belongs to the user's 
        return obj.shop.user == request.user