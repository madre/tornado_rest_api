#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from RestFramework.handlers import RESTHandler


class HelloHandler(RESTHandler):
    AUTH_CHECK = False

    def get(self, *args, **kwargs):
        arguments = self.request.DATA  # 请求参数
        te = {"tes": "ew", "arguments": arguments}
        self.write(te)  # 未使用异步调用时，使用self.write

    @gen.coroutine
    def post(self, *args, **kwargs):
        url = "http://api.leyingke.com/lyk_new/v1/util/province/"
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(url)
        self._response(response.body)  # 异步调用时，使用self._response

    @gen.coroutine
    def put(self, *args, **kwargs):
        url = "http://api.leyingke.com/lyk_new/v1/util/province/"
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(url)
        self._response(response.body)  # 异步调用时，使用self._response