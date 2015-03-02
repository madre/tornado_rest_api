# -*- coding: utf-8 -*-


class UserCenterBackend(object):
    def authenticate(self, request, **kwargs):
        # TODO: need to add how to authenticate user, if user center doesn't return User, return None
        return None


class Authentication(object):
    backend = UserCenterBackend()

    def __init__(self, *args, **kwargs):
        backend = kwargs.pop('backend', None)
        if backend is not None:
            self.backend = backend

    def is_authenticated(self, request, **kwargs):
        user = self.backend.authenticate(request, **kwargs)
        return bool(user), user
