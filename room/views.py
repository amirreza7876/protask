from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status
from room.models import JoinRequest, Room, InviteRequest
from room.serializers import RoomSerializer, JoinRequestSerializer, InviteRequestSerializer
from room.utils.is_valid_email import is_valid
from room.permissions import IsMember, IsOwner
from user.serializer import UserSerializer
from user.models import CustomUser


class UpdateName(UpdateAPIView):
    lookup_field = 'id'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsOwner,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get("name")
        instance.save()
        return Response({'msg': 'updated'})


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
    lookup_field = 'id'
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsMember]
    queryset = Room.objects.all()

    def get_serializer_context(self):
        context = super(RoomDetailApi, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class RemoveUserFromBoard(UpdateAPIView):
    lookup_field = 'id'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsOwner,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        username = request.data.get('username')
        user = CustomUser.objects.get(username=username)
        if instance.leader == user:
            return Response({"msg": "error"}, status=status.HTTP_400_BAD_REQUEST)
        instance.members.remove(user)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class LeaveBoard(UpdateAPIView):
    lookup_field = 'id'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        instance.members.remove(user)
        return Response({'msg': "left successfully"})


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

        # is_valid() returns True if format of username_or_email matches with email
        is_email = is_valid(username_or_email)
        target_user = get_object_or_404(CustomUser, email=username_or_email) if is_email else \
            get_object_or_404(CustomUser, username=username_or_email)

        if target_user not in room_members:
            invite_object = InviteRequest.objects.get_or_create(for_user=target_user, from_room=room)
            invite_object_model = invite_object[0]
            invite_status = invite_object_model.status
            invite_already_exist = invite_object[1]
            if not invite_already_exist and invite_status == 'r':
                invite_object_model.status = 'p'
                invite_object_model.save()
                return Response({"msg": "request sent"}, status=status.HTTP_201_CREATED)
            if invite_already_exist:
                return Response({"msg": "request sent"}, status=status.HTTP_201_CREATED)
            return Response({'msg': 'already invited user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': "already member"}, status=status.HTTP_403_FORBIDDEN)

        #
        # if target_user in room_members:
        #     return Response({'error': "already member"}, status=status.HTTP_400_BAD_REQUEST)
        #
        # InviteRequest.objects.create(from_room=room, for_user=target_user)
        # return Response({'data': 'invitation sent'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_request_list(request, uuid):
    print('helloooo')
    room = get_object_or_404(Room, id=uuid)
    room_members = room.members.all()
    user = request.user
    if user in room_members:
        room_requests = JoinRequest.objects.filter(for_room=room)
        serializer = JoinRequestSerializer(room_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"msg": "error"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_invite_list(request, uuid):
    room = get_object_or_404(Room, id=uuid)
    room_members = room.members.all()
    user = request.user
    if user in room_members:
        room_requests = InviteRequest.objects.filter(from_room=room)
        serializer = InviteRequestSerializer(room_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"msg": "error"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_invite_status(request):
    invite_is_accepted = request.data.get('accepted')
    room_uuid = request.data.get('uuid')
    for_user = request.data.get('forUser')
    invite_id = request.data.get('inviteId')
    email = for_user['email']
    username = for_user['username']
    room = get_object_or_404(Room, id=room_uuid)
    user = get_object_or_404(CustomUser, username=username, email=email)

    if invite_is_accepted:
        room.members.add(user)
        invite_object = InviteRequest.objects.get(id=invite_id, from_room=room)
        invite_object.accepted = True
        invite_object.status = 'a'
        invite_object.save()
        return Response({"msg": 'accepted'}, status=status.HTTP_200_OK)
    else:
        invite_object = InviteRequest.objects.get(id=invite_id, from_room=room)
        invite_object.accepted = False
        invite_object.status = 'r'
        invite_object.save()
        return Response({"msg": 'rejected'}, status=status.HTTP_200_OK)


@api_view(['POST', 'PATCH'])
def create_room(request):
    if request.method == 'POST':
        room_name = request.data.get('name')
        room_leader = request.user
        room = Room(name=room_name, leader=room_leader)
        room.save()
        room.members.add(room_leader)
        serializer = RoomSerializer(room, context={'request': request})
        return Response(serializer.data)

    if request.method == 'PATCH':
        pass
