from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, user_request, room_request, change_request_status

router = DefaultRouter()
router.register('mine', RoomViewSet, basename='rooms')
urlpatterns = router.urls

urlpatterns += [
    path('join-requests/', user_request, name='user-request'),
    path('room-requests/<int:room_id>/<str:room_string>/', room_request, name='room-request'),
    path('request/', change_request_status, name='change-status')
]
