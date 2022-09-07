from rest_framework import permissions


class IsMember(permissions.BasePermission):
    edit_methods = ("GET",)

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user in obj.members.all():
            return True
        return False


# class IsNotMember(permissions.BasePermission):
#     edit_methods = ("POST", )
#
#     def has_permission(self, request, view):
#         print('has perm')
#         if request.user.is_authenticated:
#             return True
#
#     def has_object_permission(self, request, view, obj):
#         print('has obj perm')
#         user = request.user
#         if user not in obj.members.all():
#             return True
#         return False
