from django.forms import model_to_dict
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from room.models import Room
from room.permissions import IsOwner
from task.models import Task
from task.serializers import TaskSerializer
from user.models import CustomUser


class UserTaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.user_tasks.all()


class RoomTaskViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        request_string = self.request.query_params['requestString']
        room_id = self.request.query_params['roomId']
        room = get_object_or_404(Room, request_string=request_string, id=room_id)
        return room.room_tasks.all()

    # @action(detail=True, methods=['get'], url_path='get_room_tasks')
    # def get_tasks(self, request, pk=None):
    #     print(request.user)
    # room_id = self.request.query_params['roomId']
    # room = get_object_or_404(Room, request_string=request_string, id=room_id)
    # return room.room_tasks.all()


@api_view(['POST'])
def create_new_task(request):
    user = request.data.get('user')
    duration = request.data.get('duration')
    title = request.data.get('title')
    difficulty = request.data.get('difficulty')
    priority = request.data.get('priority')
    board_id = request.data.get('id')

    user = get_object_or_404(CustomUser, username=user)
    board = get_object_or_404(Room, id=board_id)

    new = Task(owner=board, user=user, duration=duration, title=title, difficulty=difficulty,
               priority=priority)
    new.status = 'dg'
    new.save()
    return Response({'msg': 'created'}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsOwner, ])
def update_task(request):
    task_id = request.data.get('id')
    value = request.data.get('value')
    field = request.data.get('field')
    task = get_object_or_404(Task, id=task_id)

    if field == 'user':
        user = get_object_or_404(CustomUser, username=value)
        task.user = user
        task.save()
    else:
        task.__setattr__(field, value)
        task.save()

    return Response({'msg': "updated"})
