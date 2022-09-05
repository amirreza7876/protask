from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, room_request

router = DefaultRouter()
router.register('mine', RoomViewSet, basename='rooms')
urlpatterns = router.urls
urlpatterns += [
    path('join-requests/', room_request, name='user-request')
]
