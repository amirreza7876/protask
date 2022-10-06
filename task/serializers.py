from rest_framework import serializers
from user.serializer import UserSerializer
from .models import Task, Phase


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Task
        fields = "__all__"
