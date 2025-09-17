from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return True
        if view.action == "create":
            return request.user.is_authenticated and request.user.role == "owner"
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff
