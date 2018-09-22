from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from . import models
from . import serializers
from .permissions import IsMember

from ..users.permissions import IsSelf, IsSelfOrReadOnly


class GroupView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsMember,)

    serializer_class = serializers.RoomSerializer
    lookup_url_kwarg = 'room_pk'

    def get_queryset(self):
        return get_object_or_404(models.Room.objects, pk=self.kwargs['room_pk'])


class GroupListView(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsSelfOrReadOnly,)

    serializer_class = serializers.RoomSerializer

    def get_queryset(self):
        groups_pk_filter = self.request.user.room_set.values_list('pk')
        rooms_in_common = models.PayWaysUser.objects.get(
            pk=self.kwargs['user_pk']
        ).room_set.filter(
            pk__in=groups_pk_filter
        )

        return rooms_in_common

    def create(self, request, *args, **kwargs):
        serializer = serializers.RoomSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status.HTTP_400_BAD_REQUEST)

        user = request.user
        room = serializer.save()

        models.Membership(user=user, room=room, is_admin=True).save()

        return Response(status.HTTP_201_CREATED)


class GroupMembersList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsMember,)

    serializer_class = serializers.MemberSerializer
    lookup_url_kwarg = 'room_pk'

    def get_queryset(self):
        room = get_object_or_404(self.request.user.room_set, pk=self.kwargs['room_pk'])
        return room.members.all()


class GroupInviteView(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsSelf,)

    serializer_class = serializers.MemberSerializer
