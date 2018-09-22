from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from . import models
from . import serializers
from . import permissions


class UserView(generics.RetrieveUpdateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsSelfOrReadOnly,)

    lookup_url_kwarg = 'user_pk'

    def get_queryset(self):
        return models.PayWaysUser.objects.filter(pk=self.kwargs['user_pk'])

    def get_serializer_class(self):
        if self.kwargs['user_pk'] == self.request.user.pk:
            return serializers.UserFullSerializer
        else:
            return serializers.UserSerializer

    # def get(self, request, pk, format=None):
    #     profile = self.get_object()
    #     is_authenticated = request.user.is_authenticated
    #
    #     if is_authenticated and pk == request.user.pk:
    #         serializer = serializers.UserFullSerializer(
    #             profile,
    #             context={"request": request},
    #         )
    #     else:
    #         serializer = serializers.UserSerializer(
    #             profile,
    #             context={"request": request}
    #         )
    #
    #     return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

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
