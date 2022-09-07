from rest_framework import serializers
from room.models import Room, JoinRequest, InviteRequest
from user.serializer import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    leader = UserSerializer()
    is_owner = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Room
        fields = "__all__"

    def get_is_owner(self, obj):
        try:
            return obj.leader == self.context['request'].user
        except KeyError:
            return False


class JoinRequestSerializer(serializers.ModelSerializer):
    for_room = RoomSerializer()
    from_user = UserSerializer()

    class Meta:
        model = JoinRequest
        fields = "__all__"


class InviteRequestSerializer(serializers.ModelSerializer):
    for_user = UserSerializer()
    from_room = RoomSerializer(fields=('name', 'id', 'request_string'))

    class Meta:
        model = InviteRequest
        fields = "__all__"
