from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RoomListApi, user_request, room_request_list, change_request_status, RoomDetailApi, create_room, \
    user_invitation, change_invite_status, room_invite_list

# router = DefaultRouter()
# router.register('mine', RoomViewSet, basename='rooms')
# urlpatterns = router.urls

urlpatterns = [
    path('mine/', RoomListApi.as_view(), name='my-rooms'),
    path('mine/<int:pk>/', RoomDetailApi.as_view(), name='my-rooms'),
    path('join-requests/', user_request, name='user-request'),
    path('join-invites/', user_invitation, name='user-invites'),
    path('room-requests/<int:room_id>/<str:request_string>/', room_request_list, name='room-request'),
    path('room-invites/<int:room_id>/<str:request_string>/', room_invite_list, name='room-request'),
    path('request/', change_request_status, name='change-request-status'),
    path('invite/', change_invite_status, name='change-invite-status'),
    path('create/', create_room, name='create-room')

]
