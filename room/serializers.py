from rest_framework import serializers
from room.models import Room, JoinRequest
from user.serializer import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    leader = UserSerializer()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_is_owner(self, obj):
        try:
            return obj.leader == self.context['request'].user
        except KeyError:
            pass


class JoinRequestSerializer(serializers.ModelSerializer):
    for_room = RoomSerializer()
    from_user = UserSerializer()

    class Meta:
        model = JoinRequest
        fields = "__all__"
