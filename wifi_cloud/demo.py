#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
import logging
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from validator import Required, Not, Truthy, Blank, InstanceOf, Equals, In, Length

from RestFramework.handlers import RESTHandler
from RestFramework.http_status import HTTP_STATUS_CREATED, HTTP_STATUS_ACCEPTED


access_log = logging.getLogger("api_access")
error_log = logging.getLogger("api_error")


class DemoHandler(RESTHandler):
    AUTH_CHECK = True  # 是否需要校验身份
    arguments_valid_rules = {
        "phone": [Required, InstanceOf(unicode), Length(11, maximum=11)],
        "password": [Required, ],
    }

    def get(self, *args, **kwargs):
        arguments = self.request.DATA  # 请求参数
        access_log.info("phone: %s, password: %s" % (arguments["phone"], arguments["password"]))
        error_log.error("f231312312332321")
        phone = arguments["phone"]
        result = {"message": "KO", "arguments": arguments}
        self._response(result)  # 无异步，也可使用 self.write

    @gen.coroutine
    def post(self, *args, **kwargs):
        access_log.info("POST request")
        arguments = self.request.DATA  # 请求参数， 兼容前端传json数据
        url = "http://api.leyingke.com/lyk_new/v1/util/province/"
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(url)
        self._response(response.body, status=HTTP_STATUS_CREATED)

    @gen.coroutine
    def put(self, *args, **kwargs):
        access_log.info("PUT request")
        url = "http://api.leyingke.com/lyk_new/v1/util/province/"
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(url)
        self._response(response.body, status=HTTP_STATUS_ACCEPTED)

    def delete(self, *args, **kwargs):
        arguments = self.request.DATA  # 请求参数
        access_log.info("delete request")
        result = {"message": "delete", "arguments": arguments}
        self._response(result, status=HTTP_STATUS_ACCEPTED)  # 无异步，也可使用 self.write