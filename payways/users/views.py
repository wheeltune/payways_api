from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from . import models
from . import serializers

from ..api.permissions import IsAuthenticated
from ..api.views import PayWaysApiView
from ..rooms.views import RoomsInCommonListView


class ContactsListView(generics.ListAPIView, PayWaysApiView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.get_request_user().contacts.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method not in SAFE_METHODS:
            return serializers.AddContactSerializer
        return serializers.UserSerializer

    def put(self, response, *args, **kwargs):
        to_user = get_object_or_404(models.PayWaysUser.objects, pk=response.data['contact_pk'])
        from_user = self.get_request_user()

        return Response(models.Friendship.objects.get_or_create(from_user=from_user, to_user=to_user))


class UserView(generics.RetrieveAPIView, PayWaysApiView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return models.PayWaysUser.objects.filter(pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.kwargs['pk'] == self.get_request_user_pk():
            return serializers.UserFullSerializer
        else:
            return serializers.UserSerializer

# class UserGroupsListView(APIView):
#     serializer_class = serializers.UserGroupsSerializer
#
#     def get_object(self, pk):
#         try:
#             return models.PayWaysUser.objects.get(pk=pk)
#         except models.PayWaysUser.DoesNotExist:
#             raise generics.Http404
#
#     def get(self, request, pk, format=None):
#         user = self.get_object(pk=pk).group_set.all()
#         return Response(user)
