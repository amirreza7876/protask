from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from room.models import Room


class IsMember(permissions.BasePermission):
    edit_methods = ("GET", 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user in obj.members.all():
            return True
        return False


class IsOwner(permissions.BasePermission):
    edit_methods = ("POST", "DELETE")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        room_leader = obj.leader
        if user == room_leader:
            return True
        return False


class IsMemberFunctional(permissions.BasePermission):
    def has_permission(self, request, view):
        room_id = request.data.get('roomId')
        room_object = get_object_or_404(Room, id=room_id)
        if room_object in request.user.user_rooms.all():
            return True
        return False


class IsOwnerFunctional(permissions.BasePermission):
    def has_permission(self, request, view):
        room_id = request.data.get('roomId')
        room_object = get_object_or_404(Room, id=room_id)
        if room_object in request.user.rooms_own.all():
            return True
        return False
