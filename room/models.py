from django.db import models
from room.constants import REQUEST_STATUS
from user.models import CustomUser
import uuid


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rooms_own', null=True)
    members = models.ManyToManyField(CustomUser, related_name='user_rooms', blank=True)
    request_string = models.CharField(max_length=100, null=True, blank=True, unique=True)
    color = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.name


class JoinRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_requests')
    accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=REQUEST_STATUS, default='p')
    for_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_requests')

    def __str__(self):
        return f'from {self.from_user} to {self.for_room}'

    class Meta:
        ordering = ['-id']


class InviteRequest(models.Model):
    from_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_invitation')
    accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=REQUEST_STATUS, default='p')
    for_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_invitation')

    def __str__(self):
        return f'from {self.from_room} to {self.for_user}'

    class Meta:
        ordering = ['-id']
