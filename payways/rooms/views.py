from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from . import models
from ..things.models import Thing
from ..things.serializers import ThingSerializer

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


class RoomThingsListView(generics.ListCreateAPIView, PayWaysApiView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsMember)

    lookup_url_kwarg = 'room_pk'

    def get_queryset(self):
        return Thing.objects.filter(from_room_id=self.kwargs['room_pk']).all()

    def get_serializer_class(self, *args, **kwargs):
        request_user_membership = get_object_or_404(
            models.Room.objects,
            pk=self.kwargs['room_pk']
        ).membership_set.get(
            user_id=self.get_request_user_pk()
        )

        if request_user_membership.is_admin:
            return serializers.RoomThingAdminSerializer
        else:
            return serializers.RoomThingSerializer

    def perform_create(self, serializer):
        request_user_pk = self.get_request_user_pk()

        additional_data = {
            'added_by_id': request_user_pk,
            'from_room_id': self.kwargs['room_pk']
        }
        if serializer.validated_data.get('buyer', None) is None:
            additional_data['buyer_id'] = request_user_pk

        serializer.save(**additional_data)
