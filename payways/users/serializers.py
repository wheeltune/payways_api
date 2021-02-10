from rest_framework import serializers, validators

from . import models


class UserField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return models.PayWaysUser.objects.all()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PayWaysUser
        fields = ('pk', 'username', 'first_name', 'last_name')


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PayWaysUser
        fields = ('pk', 'username', 'first_name', 'last_name', 'telegram_id', 'vk_id')
