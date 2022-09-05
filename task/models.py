from django.db import models
from task.constants import TASK_DIFFICULTY, TASK_STATUS, TASK_PRIORITY
from user.models import CustomUser
from room.models import Room


class Task(models.Model):
    owner = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name='room_tasks')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='user_tasks')
    title = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    difficulty = models.CharField(max_length=2, choices=TASK_DIFFICULTY)
    status = models.CharField(max_length=2, choices=TASK_STATUS)
    priority = models.CharField(max_length=2, choices=TASK_PRIORITY)

    def __str__(self):
        return f'{self.title} assigned to {self.user}'
