from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.role=='admin'))

    '''def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or request.user.role=='admin')'''