from rest_framework import serializers, validators

from .models import PayWaysUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayWaysUser
        fields = ('pk', 'username', 'first_name', 'last_name')


class AddContactSerializer(serializers.Serializer):
    contact_pk = serializers.IntegerField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayWaysUser
        fields = ('pk', 'username', 'first_name', 'last_name', 'telegram_id', 'vk_id')
