from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from . import models
from . import serializers
from .permissions import IsAuthenticated, IsAdminOrReadOnlyForMember, IsMember

from ..api.views import PayWaysApiView


class RoomView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnlyForMember)

    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()
    lookup_url_kwarg = 'room_pk'


class RoomsListView(generics.ListCreateAPIView, PayWaysApiView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.RoomSerializer

    def get_queryset(self):
        return self.get_request_user().room_set.all()

    def create(self, request, *args, **kwargs):
        serializer = serializers.RoomSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status.HTTP_400_BAD_REQUEST)

        user = request.user
        room = serializer.save()

        models.Membership(user=user, room=room, is_admin=True).save()

        return Response(status.HTTP_201_CREATED)


class RoomsInCommonListView(RoomsListView):
    def get_queryset(self):
        request_user_group_pks = super().get_queryset().values_list('pk')

        print(request_user_group_pks)

        rooms_in_common = get_object_or_404(
            models.PayWaysUser.objects,
            pk=self.kwargs['user_pk']
        ).room_set.filter(
            pk__in=request_user_group_pks
        )

        print(rooms_in_common, self.kwargs['user_pk'])

        return rooms_in_common


class RoomMembersListView(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsMember)

    serializer_class = serializers.UserSerializer
    lookup_url_kwarg = 'room_pk'

    def get_queryset(self):
        room = get_object_or_404(self.request.user.room_set, pk=self.kwargs['room_pk'])
        return room.members.all()

#
# class GroupInviteView(generics.CreateAPIView):
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     serializer_class = serializers.MemberSerializer
