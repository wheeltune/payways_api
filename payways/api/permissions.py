from django.shortcuts import get_object_or_404

from rest_framework import permissions

from . import models


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):  # TODO for bot authorization
        if 'request_user_pk' in view.kwargs:
            get_object_or_404(
                models.PayWaysUser.objects,
                pk=view.kwargs['request_user_pk']
            )
            return True
        return super().has_permission(request, view)


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):  # TODO for bot authorization
        return super().has_permission(request, view)
