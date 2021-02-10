from django.shortcuts import get_object_or_404

from rest_framework.permissions import BasePermission, SAFE_METHODS

from . import models
from ..api.permissions import IsAuthenticated


class IsRelatedRoomMember(BasePermission):
    def get_request_user_pk(self, request, view):
        return view.kwargs.get('request_user_pk', request.user.pk)

    def has_permission(self, request, view):
        if 'kwargs' not in dir(self) or 'room_pk' not in self.kwargs:
            return False
        thing = get_object_or_404(
            models.Thing.objects,
            pk=view.kwargs['thing_pk']
        )

        request_user_pk = self.get_request_user_pk(request, view)
        return thing.from_room.membership_set.filter(
            user_id=request_user_pk
        ).exists()


class IsAdminOrBuyerOrReadOnlyForRelatedRoomMember(BasePermission):
    def get_request_user_pk(self, request, view):
        return view.kwargs.get('request_user_pk', request.user.pk)

    def has_permission(self, request, view):
        if 'kwargs' not in dir(self) or 'room_pk' not in self.kwargs:
            return False
        thing = get_object_or_404(
            models.Thing.objects,
            pk=view.kwargs['thing_pk']
        )

        try:
            request_user_pk = self.get_request_user_pk(request, view)
            user_membersthip = thing.from_room.membership_set.get(
                user_id=request_user_pk
            )

            return (user_membersthip.is_admin or thing.buyer_id == request_user_pk) or request.method in SAFE_METHODS
        except models.Membership.DoesNotExist:
            return False
