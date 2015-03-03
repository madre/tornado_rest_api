#!/usr/bin/env python
# coding=utf-8
"""
身份认证
__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""


class UserCenterBackend(object):
    def basic_auth(self, request, **kwargs):
        # TODO: 添加基本身份认证
        return None

    def token_auth(self, request, **kwargs):
        # TODO: 添加token身份认证
        return None


class Authentication(object):
    backend = UserCenterBackend()

    def __init__(self, *args, **kwargs):
        backend = kwargs.pop('backend', None)
        if backend is not None:
            self.backend = backend

    def is_authenticated(self, request, **kwargs):
        user = self.backend.basic_auth(request, **kwargs)
        return bool(user), user
