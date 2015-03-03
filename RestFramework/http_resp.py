#!/usr/bin/env python
# coding=utf-8
"""
http返回状态定义
__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""

import tornado.httpclient
from http_status import RESPONSES
from http_status import HTTP_STATUS_OK, HTTP_STATUS_CREATED, HTTP_STATUS_ACCEPTED, \
    HTTP_STATUS_NOT_MODIFIED


class HttpResponse(tornado.httpclient.HTTPResponse):
    code = HTTP_STATUS_OK

    def __init__(self, request, data=None, *args, **kwargs):
        url = getattr(request, 'url', request.uri)
        setattr(request, 'url', url)
        super(HttpResponse, self).__init__(request, self.code, *args, **kwargs)
        message = RESPONSES[self.code]
        self._body = data or {"message": message, "code": self.code}


# 以下为主要的几个Http成功
class HttpCreated(HttpResponse):
    # POST 创建数据成功
    code = HTTP_STATUS_CREATED

    def __init__(self, *args, **kwargs):
        location = kwargs.pop('location', None)
        super(HttpCreated, self).__init__(*args, **kwargs)
        if location is not None:
            self.headers['Location'] = location


class HttpOk(HttpResponse):
    # GET 请求数据成功
    code = HTTP_STATUS_OK


class HttpAccepted(HttpResponse):
    # PUT 修改数据成功
    code = HTTP_STATUS_ACCEPTED


class HttpNotModified(HttpResponse):
    # http 304 数据未修改，请使用缓存
    code = HTTP_STATUS_NOT_MODIFIED
