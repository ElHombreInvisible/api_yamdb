from rest_framework.permissions import BasePermission

ADMIN = 'admin'


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):

        return bool(request.user.is_authenticated
                    and (request.user.is_staff
                         or request.user.role == ADMIN))
