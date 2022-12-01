from django.db import models


class RequestTypes(models.TextChoices):
    PENDING = "P", "Pending"
    ACCEPTED = "A", "Accepted"
    REJECTED = "R", "REJECTED"
