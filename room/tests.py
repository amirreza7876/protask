from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
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

    def test_unauthorized_request_for_room_list(self):
        url = reverse('room-detail', kwargs={'id': self.room.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)