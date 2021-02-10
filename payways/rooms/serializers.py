from collections import OrderedDict
from rest_framework import serializers

from payways.users.serializers import UserField, UserSerializer
from payways.users.models import PayWaysUser
from payways.things.models import Thing, Useship

from . import models


class RoomMemberField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return models.Room.objects.get(pk=self.context['view'].kwargs['room_pk']).members.all()


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('id', 'name',)


class AddRoomSerializer(serializers.ModelSerializer):
    members = UserField(many=True)

    class Meta:
        model = models.Room
        fields = ('name', 'members',)

    def create(self, validated_data):
        from_user = validated_data.pop('from_user')
        members = validated_data.pop('members')
        instance = super().create(validated_data)

        models.Membership.objects.filter(room_id=instance.pk).delete()
        models.Membership(user=from_user, room=instance, is_admin=True).save()
        for user in members:
            models.Membership(user=user, room=instance, is_admin=False).save()

        return instance


class RoomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayWaysUser
        fields = ('id', 'first_name', 'last_name')


class RoomUseshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Useship
        fields = ('user_id', 'weight')


class RoomThingSerializer(serializers.ModelSerializer):
    buyer = RoomMemberField()
    added_by = RoomMemberField(read_only=True)

    class Meta:
        model = Thing
        fields = ('id', 'name', 'cost', 'added_by', 'buyer')


class RoomThingPostSerializer(serializers.ModelSerializer):
    used_by = RoomMemberField(many=True)
    buyer = RoomMemberField()
    added_by = RoomMemberField(read_only=True)

    class Meta:
        model = Thing
        fields = ('id', 'name', 'cost', 'added_by', 'buyer', 'used_by')

    def create(self, validated_data):
        used_by = validated_data.pop('used_by')
        instance = super().create(validated_data)

        Useship.objects.filter(thing_id=instance.pk).delete()

        weight = 1 / len(used_by)
        for user in used_by:
            Useship(thing=instance, user=user, weight=weight).save()

        return instance


class RoomBalanceSerializer(serializers.Serializer):
    balance = serializers.FloatField()


# class RoomThingAdminSerializer(RoomThingSerializer):
#     buyer = RoomMemberField(allow_null=True, allow_empty=False)
