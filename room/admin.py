from django.contrib import admin
from room.models import Room, JoinRequest, InviteRequest

admin.site.register(Room)
admin.site.register(JoinRequest)
admin.site.register(InviteRequest)
