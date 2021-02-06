from django.shortcuts import get_object_or_404

from rest_framework.permissions import BasePermission, SAFE_METHODS

from . import models
from ..api.permissions import IsAuthenticated


class IsMember(BasePermission):
    def get_request_user(self, request, view):
        if 'request_user_pk' in view.kwargs:
            return get_object_or_404(
                models.PayWaysUser.objects,
                pk=view.kwargs['request_user_pk']
            )
        else:
            return request.user

    def has_permission(self, request, view):
        return self.get_request_user(request, view).membership_set.filter(
            room_id=view.kwargs["room_pk"]
        ).exists()


class IsAdminOrReadOnlyForMember(BasePermission):
    def get_request_user(self, request, view):
        if 'request_user_pk' in view.kwargs:
            return get_object_or_404(
                models.PayWaysUser.objects,
                pk=view.kwargs['request_user_pk']
            )
        else:
            return request.user

    def has_permission(self, request, view):
        try:
            user_membership = self.get_request_user(request, view).membership_set.get(
                room_id=view.kwargs["room_pk"]
            )
        except models.Membership.DoesNotExist:
            return False

        return user_membership.is_admin or request.method in SAFE_METHODS

# class IsAdminOrReadOnly(BasePermission):
#     def get_request_user_pk(self, request, view):
#         return view.kwargs.get('request_user_pk', request.user.pk)
#
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS or models.Room.objects.get(
#             pk=view.kwargs["group_pk"]
#         ).members.filter(user_pk=self.get_request_user_pk(request, view)).is_admin
