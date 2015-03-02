# -*- coding: utf-8 -*-
from RestFramework import http


class APIError(Exception):
    pass


class ImmediateHttpResponse(APIError):
    def __init__(self, response, data=None):
        self._response = response

    @property
    def response(self):
        return self._response


class APIResponseError(APIError):
    response_class = http.HttpResponse

    def __init__(self, request, data=None, **kwargs):
        self._response = self.response_class(request, data, **kwargs)

    @property
    def response(self):
        return self._response

    def __str__(self):
        return str(self._response._body)


class HttpBadRequest(APIResponseError):
    response_class = http.HttpBadRequest


class HttpUnauthorized(APIResponseError):
    response_class = http.HttpUnauthorized


class HttpForbidden(APIResponseError):
    response_class = http.HttpForbidden


class HttpNotFound(APIResponseError):
    response_class = http.HttpNotFound


class HttpMethodNotAllowed(APIResponseError):
    response_class = http.HttpMethodNotAllowed


class HttpUnprocessableEntity(APIResponseError):
    response_class = http.HttpUnprocessableEntity


class HttpApplicationError(APIResponseError):
    response_class = http.HttpApplicationError


class MissingParamError(HttpUnprocessableEntity):
    def __init__(self, request, param_name, *args, **kwargs):
        error_data = {
            'message': "Missing `{}` param".format(param_name)
        }
        super(MissingParamError, self) \
            .__init__(request, error_data, *args, **kwargs)
