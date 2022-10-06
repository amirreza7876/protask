from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserTaskViewSet, RoomTaskViewSet, create_new_task, update_task, RoomPhaseViewSet

router = DefaultRouter()
router.register('user-tasks', UserTaskViewSet, basename='user-tasks')
router.register('room-tasks', RoomTaskViewSet, basename='room-tasks')
router.register('room-phases', RoomPhaseViewSet, basename='room-phases')
urlpatterns = router.urls

urlpatterns += [
    path('create/', create_new_task, name='create-task'),
    path('update/', update_task, name='create-task'),
]
