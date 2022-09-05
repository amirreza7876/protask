from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from task.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.user_tasks.all()
