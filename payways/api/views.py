from django.shortcuts import get_object_or_404

from . import models


class PayWaysApiView(object):
    def get_request_user_pk(self):
        return self.kwargs.get('request_user_pk', self.request.user.pk)

    def get_request_user(self):
        if 'request_user_pk' in self.kwargs:
            return get_object_or_404(
                models.PayWaysUser.objects,
                pk=self.kwargs['request_user_pk']
            )
        else:
            return self.request.user
