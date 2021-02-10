from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from . import models
from . import serializers
from .permissions import IsAuthenticated, IsAdminOrBuyerOrReadOnlyForRelatedRoomMember, IsRelatedRoomMember


class ThingView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrBuyerOrReadOnlyForRelatedRoomMember)

    serializer_class = serializers.ThingSerializer
    queryset = models.Thing.objects.all()
    lookup_url_kwarg = 'thing_pk'


class ThingsListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsRelatedRoomMember)

    serializer_class = serializers.ThingSerializer
    lookup_url_kwarg = 'thing_pk'

    def get_queryset(self):
        return get_object_or_404(
            models.Room.objects,
            pk=self.kwargs['room_pk']
        ).things_set.all()
