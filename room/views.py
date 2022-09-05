from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from room.models import JoinRequest, Room
from room.serializers import RoomSerializer, JoinRequestSerializer


class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.user_rooms.all()

    def get_serializer_context(self):
        context = super(RoomViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


@api_view(['GET', 'POST'])
def room_request(request):
    if request.method == 'GET':
        if not request.user.is_anonymous:
            requests = JoinRequest.objects.filter(from_user=request.user)
            serializer = JoinRequestSerializer(data=requests, many=True)
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"data": "login first"}, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'POST':
        # room members cant request again to the same room
        if not request.user.is_anonymous:
            user = request.user
            request_string = request.data['request_string']
            try:
                room = Room.objects.get(request_string=request_string)
            except ObjectDoesNotExist:
                return Response({"msg": "room does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if user not in room.members.all():
                request_object = JoinRequest.objects.get_or_create(from_user=user, for_room=room)
                if request_object[1]:
                    return Response({"msg": "request sent"}, status=status.HTTP_201_CREATED)
                return Response({'msg': 'already requested to join'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg": "already member"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': "login first"}, status=status.HTTP_401_UNAUTHORIZED)
