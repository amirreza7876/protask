from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from room.models import Room
from room.utils.generate_color import generate_color
from room.utils.random_string import get_random_string


@receiver(pre_save, sender=Room)
def create_request_string(sender, instance, *args, **kwargs):
    if instance.request_string is None:
        instance.request_string = get_random_string(10)


@receiver(pre_save, sender=Room)
def create_background_color(sender, instance, *args, **kwargs):
    if instance.color == '#000000':
        instance.color = generate_color()
