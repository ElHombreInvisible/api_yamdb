from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        
        return bool(request.user.is_authenticated and (request.user.is_staff or request.user.role=='admin'))

    def has_object_permission(self, request, view, obj):

        return bool(request.user.is_authenticated and (request.user.is_staff or request.user.role=='admin'))


class IsOwner(BasePermission):

        def has_object_permission(self, request, view, obj):

            return bool(request.user==obj.user)