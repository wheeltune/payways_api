from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsSelf(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
               request.user.pk == view.kwargs['user_pk']


class IsSelfOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
               (request.method in SAFE_METHODS or request.user.pk == view.kwargs['user_pk'])
