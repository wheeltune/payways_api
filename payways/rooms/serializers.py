from collections import OrderedDict
from rest_framework import serializers

from . import models
from ..users.serializers import UserSerializer
from ..things.models import Thing, Useship


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('id', 'name',)


class RoomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PayWaysUser
        fields = ('id', 'first_name', 'last_name')


class RoomUseshipSerializer(serializers.ModelSerializer):


    class Meta:
        model = Useship
        fields = ('user_id', 'user.first_name', 'user.last_name', 'weight')


class RoomMemberField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return models.Room.objects.get(pk=self.context['view'].kwargs['room_pk']).members.all()

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        serializer = RoomUserSerializer(value)
        return serializer.data

    # Below code is copied from rest_framework.serializers.RelatedField
    # because we need to override the keys in the return value
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                # This is the only line that differs
                # from the RelatedField's implementation
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])


class RoomThingSerializer(serializers.ModelSerializer):
    used_by = RoomUseshipSerializer(source='useship_set', many=True)
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
