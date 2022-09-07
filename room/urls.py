from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RoomListApi, user_request, room_request, change_request_status, RoomDetailApi, create_room

# router = DefaultRouter()
# router.register('mine', RoomViewSet, basename='rooms')
# urlpatterns = router.urls

urlpatterns = [
    path('mine/', RoomListApi.as_view(), name='my-rooms'),
    path('mine/<int:pk>/', RoomDetailApi.as_view(), name='my-rooms'),
    path('join-requests/', user_request, name='user-request'),
    path('room-requests/<int:room_id>/<str:room_string>/', room_request, name='room-request'),
    path('request/', change_request_status, name='change-status'),
    path('create/', create_room, name='create-room')

]
