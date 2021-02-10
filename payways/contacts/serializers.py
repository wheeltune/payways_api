from rest_framework import serializers, validators

from payways.users.models import Friendship


class AddContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friendship
        fields = ('to_user',)
