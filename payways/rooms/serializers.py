from rest_framework import serializers

from . import models


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('pk', 'name',)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PayWaysUser
        fields = ('pk', 'first_name',)
