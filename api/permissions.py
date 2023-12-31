from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.method in permissions.SAFE_METHODS and request.user.is_authenticated or request.user.is_staff
