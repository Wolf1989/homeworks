from rest_framework.permissions import SAFE_METHODS, BasePermission

from advertisements.models import Advertisement

class IsAuthenticatedUser(BasePermission):
    """Авторизация для всех запросов"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated)

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.creator == request.user)