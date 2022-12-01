from django.db import models
from task.enums import TaskDifficultyChoices, TaskStatusChoices, TaskPriorityChoices
from room.models import Room
from django.conf import settings


class Phase(models.Model):
    name = models.CharField(max_length=250, null=True)
    board = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name='room_phases')

    def __str__(self):
        return f'phase {self.name} / board {self.board.name}'


class Task(models.Model):
    owner = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name='room_tasks')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, null=True, related_name='phase_tasks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_tasks')
    title = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    duration = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=2, choices=TaskDifficultyChoices.choices)
    status = models.CharField(max_length=2, default='a', choices=TaskStatusChoices.choices)
    priority = models.CharField(max_length=2, choices=TaskPriorityChoices.choices)

    def __str__(self):
        return f'{self.title} assigned to {self.user}'
