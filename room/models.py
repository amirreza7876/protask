import uuid
from django.db import models
from django.conf import settings
from .enums import RequestTypes


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rooms_own', null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_rooms', blank=True)
    request_string = models.CharField(max_length=100, null=True, blank=True, unique=True)
    color = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.name


class RequestAble(models.Model):
    accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=RequestTypes.choices, default=RequestTypes.PENDING)

    class Meta:
        abstract = True


class JoinRequest(RequestAble):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_requests')
    for_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_requests')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'from {self.from_user} to {self.for_room}'


class InviteRequest(RequestAble):
    from_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_invitation')
    for_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_invitation')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'from {self.from_room} to {self.for_user}'
