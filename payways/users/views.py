from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from payways.api.permissions import IsAuthenticated
from payways.api.views import PayWaysApiView
from payways.rooms.views import RoomsInCommonListView

from . import models
from . import serializers


class UserView(generics.RetrieveAPIView, PayWaysApiView):
    permission_classes = (IsAuthenticated, )
    lookup_url_kwarg = 'user_pk'

    def get_queryset(self):
        return models.PayWaysUser.objects.filter(pk=self.kwargs['user_pk'])

    def get_serializer_class(self):
        if self.kwargs['user_pk'] == self.get_request_user_pk():
            return serializers.UserFullSerializer
        else:
            return serializers.UserSerializer


class UsersSearchView(generics.ListAPIView, PayWaysApiView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return models.PayWaysUser.objects.filter(username__startswith=query).all()

    def get_serializer_class(self, *args, **kwargs):
        return serializers.UserSerializer
