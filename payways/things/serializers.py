from rest_framework import serializers
from rest_framework.request import Request

from . import models


class MemberField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        thing_instance = models.Thing.objects.get(pk=self.context['view'].kwargs['thing_pk'])
        return thing_instance.from_room.members.all()


class ThingSerializer(serializers.ModelSerializer):
    used_by = MemberField(many=True)
    buyer = MemberField()
    added_by = MemberField(read_only=True)

    class Meta:
        model = models.Thing
        fields = ('id', 'name', 'cost', 'buyer', 'used_by', 'added_by')

    def update(self, instance, validated_data):
        models.Useship.objects.filter(thing_id=instance.pk).delete()
        for user in validated_data.pop('used_by'):
            models.Useship(thing=instance, user=user, weight=1.0).save()

        return super().update(instance, validated_data)
