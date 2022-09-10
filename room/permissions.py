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


class IsOwner(permissions.BasePermission):
    edit_methods = ("POST",)

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        room_leader = obj.leader
        if user == room_leader:
            return True
        return False