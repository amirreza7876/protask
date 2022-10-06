from django.db import models
from task.constants import TASK_DIFFICULTY, TASK_STATUS, TASK_PRIORITY
from user.models import CustomUser
from room.models import Room


class Phase(models.Model):
    name = models.CharField(max_length=250, null=True)
    board = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name='room_phases')

    def __str__(self):
        return f'phase {self.name} / board {self.board.name}'


class Task(models.Model):
    owner = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name='room_tasks')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, null=True, related_name='phase_tasks')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_tasks')
    title = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    difficulty = models.CharField(max_length=2, choices=TASK_DIFFICULTY)
    duration = models.IntegerField(default=0)
    status = models.CharField(max_length=2, default='a', choices=TASK_STATUS)
    priority = models.CharField(max_length=2, choices=TASK_PRIORITY)

    def __str__(self):
        return f'{self.title} assigned to {self.user}'
