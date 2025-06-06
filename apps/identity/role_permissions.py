from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to users with role 'admin'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsExternal(BasePermission):
    """
    Allows access only to users with role 'external'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'external'
