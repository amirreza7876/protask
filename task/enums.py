from django.db import models


class TaskPriorityChoices(models.TextChoices):
    LOW = 'L', 'Low'
    MEDIUM = 'ME', 'Medium'
    MAJOR = 'MA', 'Major'
    SHOWSTOPPER = 'SH', 'Showstopper'


class TaskStatusChoices(models.TextChoices):
    ASSIGNING = 'A', 'Assigning'
    DONE = 'D', 'Done'
    DOING = 'DG', 'Doing'
    STUCK = 'S', 'Stuck'
    TESTING = 'T', 'Testing'


class TaskDifficultyChoices(models.TextChoices):
    EASy = 'E', 'Easy'
    ELEMENTARY = 'EL', 'Elementary'
    MEDIUM = 'M', 'Medium'
    HARD = 'H', 'Hard'
