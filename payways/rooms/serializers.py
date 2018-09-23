from rest_framework import serializers

from . import models
from ..users.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('id', 'name',)
