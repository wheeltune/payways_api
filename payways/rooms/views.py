from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS

from payways.api.views import PayWaysApiView
from payways.things.models import Thing, Useship
from payways.things.serializers import ThingSerializer

from . import serializers
from . import models
from . import permissions


class RoomView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsMember)

    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()
    lookup_url_kwarg = 'room_pk'


class RoomsListView(generics.ListCreateAPIView, PayWaysApiView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.get_request_user().room_set.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method not in SAFE_METHODS:
            return serializers.AddRoomSerializer
        return serializers.RoomSerializer

    def perform_create(self, serializer):
        additional_data = {
            'from_user': self.get_request_user(),
        }
        serializer.save(**additional_data)


class RoomsInCommonListView(RoomsListView):
    def get_queryset(self):
        request_user_group_pks = super().get_queryset().values_list('pk')

        rooms_in_common = get_object_or_404(
            models.PayWaysUser.objects,
            pk=self.kwargs['user_pk']
        ).room_set.filter(
            pk__in=request_user_group_pks
        )
        return rooms_in_common


class RoomMembersListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsMember)

    serializer_class = serializers.UserSerializer
    lookup_url_kwarg = 'room_pk'

    def get_queryset(self):
        room = get_object_or_404(self.request.user.room_set, pk=self.kwargs['room_pk'])
        return room.members.all()


class RoomThingsListView(generics.ListCreateAPIView, PayWaysApiView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsMember)

    lookup_url_kwarg = 'room_pk'

    def get_queryset(self):
        return Thing.objects.filter(from_room__pk=self.kwargs['room_pk']).all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return serializers.RoomThingPostSerializer
        # request_user_membership = get_object_or_404(
        #     models.Room.objects,
        #     pk=self.kwargs['room_pk']
        # ).membership_set.get(
        #     user_id=self.get_request_user_pk()
        # )

        # if request_user_membership.is_admin:
        #     return serializers.RoomThingAdminSerializer
        # else:
        return serializers.RoomThingSerializer

    def perform_create(self, serializer):
        request_user_pk = self.get_request_user_pk()

        additional_data = {
            'added_by_id': request_user_pk,
            'from_room_id': self.kwargs['room_pk']
        }
        if serializer.validated_data.get('buyer', None) is None:
            additional_data['buyer_id'] = request_user_pk
        if not serializer.validated_data.get('used_by', None):
            memberships = Membership.objects.filter(room__pk=self.kwargs['room_pk']).all()
            additional_data['used_by'] = list(map(lambda _: _.user, memberships))

        serializer.save(**additional_data)


class Balance:
    def __init__(self, balance):
        self.balance = balance


class RoomBalanceView(APIView, PayWaysApiView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsMember)

    def get(self, request, room_pk):
        request_user_pk = self.get_request_user_pk()

        room_things = Thing.objects.filter(from_room__pk=room_pk)
        bought_things = room_things.filter(buyer__pk=request_user_pk)
        spent = sum(map(lambda _: _.cost, bought_things))

        useships = Useship.objects.filter(user__pk=request_user_pk, thing__in=room_things).all()
        used = sum(map(lambda _: _.weight * _.thing.cost, useships))

        serializer = serializers.RoomBalanceSerializer(Balance(spent - used))
        return Response(serializer.data)
