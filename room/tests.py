from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Count
from .models import Room

CustomUser = get_user_model()


class RoomTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username='testuser',
                                                  email='testuser@gmail.com',
                                                  password='testpassword')
        cls.room = Room.objects.create(name='test room',
                                       leader=cls.user)

    def test_room_created(self):
        self.assertEqual(self.room.name, 'test room')
        self.assertEqual(self.room.leader, self.user)
        self.assertNotEqual(self.room.request_string, None)
        self.assertNotEqual(self.room.color, None)
