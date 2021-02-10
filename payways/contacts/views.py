from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS

from payways.api.permissions import IsAuthenticated
from payways.api.views import PayWaysApiView
from payways.users.serializers import UserSerializer

from . import serializers


class ContactsListView(generics.ListCreateAPIView, PayWaysApiView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.get_request_user().contacts.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method not in SAFE_METHODS:
            return serializers.AddContactSerializer
        return UserSerializer

    def perform_create(self, serializer):
        additional_data = {
            'from_user': self.get_request_user(),
        }
        serializer.save(**additional_data)
