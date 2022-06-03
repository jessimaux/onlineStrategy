from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from accounts.models import Account
from django.http import Http404


# TODO: WHAT IS THIS? ITS REALLY NEED? LOGINREQUIREDMIXIN OR THAT? USE IN accounts/views
class AuthenticationPermissionsMixin:
    def has_permissions(self):
        return not self.request.user.is_authenticated

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return HttpResponseRedirect(reverse_lazy('index'))
        return super().dispatch(request, *args, **kwargs)


class MethodistPermissionsMixin:
    def has_permissions(self):
        return Account.objects.get(id=self.request.user.id).methodist

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ModeratorPermissionsMixin:
    def has_permissions(self):
        return Account.objects.get(id=self.request.user.id).moderator

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404
        return super().dispatch(request, *args, **kwargs)