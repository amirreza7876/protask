from rest_framework.routers import DefaultRouter
from .views import UserTaskViewSet, RoomTaskViewSet

router = DefaultRouter()
router.register('user-tasks', UserTaskViewSet, basename='user-tasks')
router.register('room-tasks', RoomTaskViewSet, basename='room-tasks')
urlpatterns = router.urls
