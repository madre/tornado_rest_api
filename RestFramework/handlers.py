#!/usr/bin/env python
# coding=utf-8
"""
基础http处理
__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
import logging
import traceback
import sys
from tornado.web import RequestHandler, HTTPError, Finish
from tornado import httputil
from tornado.log import gen_log
from tornado.escape import json_decode

from RestFramework import auth
from RestFramework import serializers
from RestFramework.exceptions import APIError
from RestFramework.http_status import HTTP_STATUS_METHOD_NOT_ALLOWED, HTTP_STATUS_UNATHORIZED, HTTP_STATUS_OK
from RestFramework.http_status import RESPONSES


access_log = logging.getLogger("api_access")
error_log = logging.getLogger("api_error")


class BaseRESTHandler(RequestHandler):
    allowed_methods = ["GET", "HEAD", "POST", "DELETE", "PATCH", "PUT",
                       "OPTIONS"]  # 定制支持的http方法
    AUTH_CHECK = False
    THROTTLE_CHECK = False
    authentication = auth.Authentication()
    serializer = serializers.JSONSerializer()
    arguments_required = []  # 定义必须上传的参数

    def __init__(self, *args, **kwargs):
        super(BaseRESTHandler, self).__init__(*args, **kwargs)
        self.current_user = None

    def cleaning(self):
        # 清理连接
        pass

    def _get_request_data(self):
        # 参数格式和匹配验证，之后单独实现类
        content_type = self.request.headers.get("Content-Type")
        if content_type and content_type == "application/json":
            # json数据较复杂，TODO: 找到检查上传的平衡方案
            self.request.DATA = json_decode(self.request.body)  # 兼容前端传json body
            for field in self.arguments_required:
                # 检查是否有必须字段
                self._get_argument(field, self._ARG_DEFAULT, self.request.DATA, True)
        else:
            data = {}
            for arg in list(self.request.arguments.keys()):
                if arg in self.arguments_required:
                    data[arg] = self.get_argument(arg)  # 必须的参数未传直接报错
                else:
                    data[arg] = self.get_argument(arg, "")
            self.request.DATA = data

    def prepare(self):
        # 预处理
        self.method_check()
        if self.AUTH_CHECK:
            self.is_authenticated()
        if self.THROTTLE_CHECK:
            self.throttle_check()

        # 将上传数据放入request.DATA中
        self._get_request_data()

    def on_finish(self):
        # 结束前处理
        self.log_throttle_access()
        self.cleaning()

    def set_default_headers(self):
        # 将默认的返回头信息设置为 json
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def _handle_request_exception(self, e):
        # 定制异常错误信息，透传错误的message
        if isinstance(e, Finish):
            if not self._finished:
                self.finish()
            return
        self.log_exception(*sys.exc_info())
        if self._finished:
            return
        if isinstance(e, HTTPError):
            if e.status_code not in httputil.responses and not e.reason:
                gen_log.error("Bad HTTP status code: %d", e.status_code)
                self.send_error(500, exc_info=sys.exc_info(), message=e.log_message)
            else:
                self.send_error(e.status_code, exc_info=sys.exc_info(), message=e.log_message)
        else:
            self.send_error(500, exc_info=sys.exc_info(), message=e.message)

    def write_error(self, status_code, **kwargs):
        """# 定制异常错误信息, 默认改为json数据
        """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'application/json')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            message = kwargs["message"] if "message" in kwargs else self._reason
            error_info = {"message": message, "code": status_code}
            self.finish(error_info)

    def _response(self, response, code=HTTP_STATUS_OK, *args, **kwargs):
        message = RESPONSES[code]
        self._body = response or {"message": message, "code": code}
        if self._finished:
            return
        self.set_status(code)
        self.finish(response)  # finish 会调用 on_finish 清理相关连接
        return

    def method_check(self):
        # 检查HTTP方法是否支持
        method = self.request.method.upper()

        allowed_methods = [meth.upper() for meth in self.allowed_methods]
        allows = ','.join(meth for meth in allowed_methods)

        if method not in self.SUPPORTED_METHODS or \
                method not in allowed_methods:
            self.set_header('Allow', allows)
            raise APIError(HTTP_STATUS_METHOD_NOT_ALLOWED,
                           log_message=RESPONSES[HTTP_STATUS_METHOD_NOT_ALLOWED])
        return method

    def serialize(self, data):
        # 数据Json序列化, 只有在json中有 datetime和Decimal 类型时，需要序列化下
        return self.serializer.serialize(data)

    def is_authenticated(self):
        # 判断用户身份
        is_auth, user = self.authentication.is_authenticated(self.request)

        if not is_auth:
            self.current_user = None
            raise APIError(HTTP_STATUS_UNATHORIZED,
                           log_message=RESPONSES[HTTP_STATUS_UNATHORIZED])
        else:
            self.current_user = user

    def throttle_check(self):
        # 访问流量控制
        pass

    def log_throttle_access(self):
        # 已完成服务的打印日志
        pass

    def head(self, *args, **kwargs):
        raise APIError(HTTP_STATUS_METHOD_NOT_ALLOWED,
                       log_message=RESPONSES[HTTP_STATUS_METHOD_NOT_ALLOWED])

    def options(self, *args, **kwargs):
        raise APIError(HTTP_STATUS_METHOD_NOT_ALLOWED,
                       log_message=RESPONSES[HTTP_STATUS_METHOD_NOT_ALLOWED])

    def get(self, *args, **kwargs):
        raise APIError(HTTP_STATUS_METHOD_NOT_ALLOWED,
                       log_message=RESPONSES[HTTP_STATUS_METHOD_NOT_ALLOWED])

    def post(self, *args, **kwargs):
        raise APIError(HTTP_STATUS_METHOD_NOT_ALLOWED,
                       log_message=RESPONSES[HTTP_STATUS_METHOD_NOT_ALLOWED])

    def put(self, *args, **kwargs):
        raise APIError(HTTP_STATUS_METHOD_NOT_ALLOWED,
                       log_message=RESPONSES[HTTP_STATUS_METHOD_NOT_ALLOWED])

    def patch(self, *args, **kwargs):
        raise APIError(HTTP_STATUS_METHOD_NOT_ALLOWED,
                       log_message=RESPONSES[HTTP_STATUS_METHOD_NOT_ALLOWED])

    def delete(self, *args, **kwargs):
        raise APIError(HTTP_STATUS_METHOD_NOT_ALLOWED,
                       log_message=RESPONSES[HTTP_STATUS_METHOD_NOT_ALLOWED])


class RESTHandler(BaseRESTHandler):
    pass
