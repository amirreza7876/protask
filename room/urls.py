from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import RoomListApi, user_request, room_request_list, change_request_status, RoomDetailApi, create_room, \
    user_invitation, change_invite_status, room_invite_list, UpdateName, RemoveUserFromBoard, LeaveBoard

urlpatterns = [
    path('edit-name/<uuid:id>', UpdateName.as_view(), name='update-room-name'),
    path('remove-member/<uuid:id>', RemoveUserFromBoard.as_view(), name='remove-member'),
    path('leave/<uuid:id>', LeaveBoard.as_view(), name='leave-board'),
    path('mine/<uuid:id>/', RoomDetailApi.as_view(), name='my-rooms'),
    path('mine/', RoomListApi.as_view(), name='my-rooms'),
    path('join-requests/', user_request, name='user-request'),
    path('join-invites/', user_invitation, name='user-invites'),
    path('room-requests/<uuid:uuid>/', room_request_list, name='room-request'),
    path('room-invites/<uuid:uuid>/', room_invite_list, name='room-request'),
    path('request/', change_request_status, name='change-request-status'),
    path('invite/', change_invite_status, name='change-invite-status'),
    path('create/', create_room, name='create-room'),
]
