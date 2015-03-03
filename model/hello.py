#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from RestFramework.handlers import RESTHandler
from RestFramework.http_status import HTTP_STATUS_CREATED, HTTP_STATUS_ACCEPTED


class HelloHandler(RESTHandler):
    AUTH_CHECK = False  # 是否需要校验身份
    arguments_required = []  # 指定必须传入的参数

    def get(self, *args, **kwargs):
        arguments = self.request.DATA  # 请求参数
        result = {"tes": "ew", "arguments": arguments}
        self._response(result)  # 无异步，也可使用 self.write

    @gen.coroutine
    def post(self, *args, **kwargs):
        arguments = self.request.DATA  # 请求参数， 兼容前端传json数据
        url = "http://api.leyingke.com/lyk_new/v1/util/province/"
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(url)
        self._response(response.body, code=HTTP_STATUS_CREATED)

    @gen.coroutine
    def put(self, *args, **kwargs):
        url = "http://api.leyingke.com/lyk_new/v1/util/province/"
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(url)
        self._response(response.body, code=HTTP_STATUS_ACCEPTED)