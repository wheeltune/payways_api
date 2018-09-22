from rest_framework.permissions import IsAuthenticated


class IsMember(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
               view.kwargs['room_pk'] in request.user.room_set.values_list('pk')
