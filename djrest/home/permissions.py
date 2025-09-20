from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsVipUser(BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated and request.user.extended.is_vip):
            return True
        raise PermissionDenied("You are not Vip user")

class IsProductOwnerPermission(BasePermission):
    #This has_object_permission will only called when Id is passed
    def has_object_permission(self, request, view, obj):
        return obj.user==request.user