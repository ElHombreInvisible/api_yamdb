from rest_framework.permissions import SAFE_METHODS, BasePermission

STAFF = ('admin', 'moderator')
ADMIN = 'admin'


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.role == ADMIN
                                                  or request.user.is_staff)


class IsStaffOrAuthor(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and ((request.user.role in STAFF)
                     or request.user.is_staff
                     or request.user == obj.author))
