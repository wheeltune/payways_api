from rest_framework import serializers, validators

from .models import PayWaysUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayWaysUser
        fields = ('pk', 'username', 'first_name', 'last_name')


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayWaysUser
        fields = ('pk', 'username', 'first_name', 'last_name', 'telegram_id', 'vk_id')
