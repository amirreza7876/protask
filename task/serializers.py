from rest_framework import serializers

from user.serializer import UserSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Task
        fields = "__all__"
