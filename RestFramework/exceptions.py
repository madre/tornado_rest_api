#!/usr/bin/env python
# coding=utf-8
"""
异常管理
__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
from RestFramework import http_resp


class APIError(Exception):
    pass


class ImmediateHttpResponse(APIError):
    def __init__(self, response, data=None):
        self._response = response

    @property
    def response(self):
        return self._response


class APIResponseError(APIError):
    response_class = http_resp.HttpResponse

    def __init__(self, request, data=None, **kwargs):
        self._response = self.response_class(request, data, **kwargs)

    @property
    def response(self):
        return self._response

    def __str__(self):
        return str(self._response._body)


class HttpBadRequest(APIResponseError):
    response_class = http_resp.HttpBadRequest


class HttpUnauthorized(APIResponseError):
    response_class = http_resp.HttpUnauthorized


class HttpForbidden(APIResponseError):
    response_class = http_resp.HttpForbidden


class HttpNotFound(APIResponseError):
    response_class = http_resp.HttpNotFound


class HttpMethodNotAllowed(APIResponseError):
    response_class = http_resp.HttpMethodNotAllowed


class HttpUnprocessableEntity(APIResponseError):
    response_class = http_resp.HttpUnprocessableEntity


class HttpApplicationError(APIResponseError):
    response_class = http_resp.HttpApplicationError


class MissingParamError(HttpUnprocessableEntity):
    def __init__(self, request, param_name, *args, **kwargs):
        error_data = {
            'message': "Missing `{}` param".format(param_name)
        }
        super(MissingParamError, self) \
            .__init__(request, error_data, *args, **kwargs)
