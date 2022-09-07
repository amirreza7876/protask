from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from room.serializers import RoomSerializer, JoinRequestSerializer, InviteRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from room.utils.is_valid_email import is_valid
from user.serializer import UserSerializer
from room.models import JoinRequest, Room, InviteRequest
from room.permissions import IsMember
from user.models import CustomUser
from rest_framework import status


class RoomListApi(ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.user_rooms.all()

    def get_serializer_context(self):
        context = super(RoomListApi, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class RoomDetailApi(RetrieveAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsMember]
    queryset = Room.objects.all()

    def get_serializer_context(self):
        context = super(RoomDetailApi, self).get_serializer_context()
        context.update({"request": self.request})
        return context


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_request(request):
    if request.method == 'GET':
        requests = JoinRequest.objects.filter(from_user=request.user)
        serializer = JoinRequestSerializer(data=requests, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        user = request.user
        request_string = request.data['request_string']
        room = get_object_or_404(Room, request_string=request_string)
        room_members = room.members.all()

        request_object = JoinRequest.objects.get_or_create(from_user=user, for_room=room)
        request_object_model = request_object[0]
        request_status = request_object_model.status
        request_already_exist = request_object[1]
        if user not in room_members:
            if not request_already_exist and request_status == 'r':
                request_object_model.status = 'p'
                request_object_model.save()
                return Response({"msg": "request sent"}, status=status.HTTP_201_CREATED)
            if request_already_exist:
                return Response({"msg": "request sent"}, status=status.HTTP_201_CREATED)
            return Response({'msg': 'already requested to join'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "already member"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_invitation(request):
    user = request.user

    if request.method == 'GET':
        invites = InviteRequest.objects.filter(for_user=user)
        serializer = InviteRequestSerializer(data=invites, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        request_string = request.data['requestString']
        username_or_email = request.data['usernameOrEmail']
        room = get_object_or_404(Room, request_string=request_string)
        room_members = room.members.all()

        if user not in room_members:
            return Response({'error': "not member"}, status=status.HTTP_403_FORBIDDEN)

        # is_valid() returns True if format of username_or_email matches with email
        is_email = is_valid(username_or_email)
        target_user = get_object_or_404(CustomUser, email=username_or_email) if is_email else \
            get_object_or_404(CustomUser, username=username_or_email)

        if target_user in room_members:
            return Response({'error': "already member"}, status=status.HTTP_400_BAD_REQUEST)

        InviteRequest.objects.create(from_room=room, for_user=target_user)
        return Response({'data': 'invitation sent'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def room_request(request, room_id, request_string):
    room = get_object_or_404(Room, request_string=request_string, id=room_id)
    room_members = room.members.all()
    user = request.user
    if user in room_members:
        room_requests = JoinRequest.objects.filter(for_room=room)
        serializer = JoinRequestSerializer(room_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"msg": "error"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def change_request_status(request):
    request_is_accepted = request.data['accepted']
    for_room = request.data['forRoom']
    from_user = request.data['fromUser']
    request_id = request.data['requestId']

    room_serializer = RoomSerializer(data=for_room)
    room_serializer.is_valid()
    room_name = room_serializer.data['name']
    request_string = room_serializer.data['request_string']
    room = Room.objects.get(request_string=request_string, name=room_name)

    user_serializer = UserSerializer(data=from_user)
    user_serializer.is_valid()
    username = user_serializer.data['username']
    email = user_serializer.data['email']
    user = CustomUser.objects.get(email=email, username=username)

    if request_is_accepted:
        room.members.add(user)
        request_object = JoinRequest.objects.get(id=request_id, for_room=room)
        request_object.accepted = True
        request_object.status = 'a'
        request_object.save()
        return Response({"msg": 'accepted'}, status=status.HTTP_200_OK)
    else:
        request_object = JoinRequest.objects.get(id=request_id, for_room=room)
        request_object.accepted = False
        request_object.status = 'r'
        request_object.save()
        return Response({"msg": 'rejected'}, status=status.HTTP_200_OK)


@api_view(['POST', 'PATCH'])
def create_room(request):
    if request.method == 'POST':
        room_name = request.data['name']
        room_leader = request.user
        room = Room(name=room_name, leader=room_leader)
        room.save()
        room.members.add(room_leader)
        serializer = RoomSerializer(room, context={'request': request})
        return Response(serializer.data)

    if request.method == 'PATCH':
        pass
