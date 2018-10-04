from rest_framework import serializers

from . import models
from ..users.serializers import UserSerializer
from ..things.models import Thing, Useship


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('id', 'name',)


class RoomMemberField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return models.Room.objects.get(pk=self.context['view'].kwargs['room_pk']).members.all()


class RoomThingSerializer(serializers.ModelSerializer):
    used_by = RoomMemberField(many=True, allow_null=False, allow_empty=False)
    buyer = RoomMemberField(read_only=True)
    added_by = RoomMemberField(read_only=True)

    class Meta:
        model = Thing
        fields = ('id', 'name', 'cost', 'buyer', 'used_by', 'added_by')

    def create(self, validated_data):
        used_by = validated_data.pop('used_by')
        instance = super().create(validated_data)

        Useship.objects.filter(thing_id=instance.pk).delete()
        for user in used_by:
            Useship(thing=instance, user=user).save()

        return instance


class RoomThingAdminSerializer(RoomThingSerializer):
    buyer = RoomMemberField(allow_null=True, allow_empty=False)
