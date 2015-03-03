#!/usr/bin/env python
# coding=utf-8
"""
异常管理
__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
import logging
from tornado.web import HTTPError


class APIError(HTTPError):
    # 需要向前端输出错误异常时，请直接使用 raise APIError() 即可
    def __init__(self, status_code, *args, **kwargs):
        super(APIError, self).__init__(status_code, *args, **kwargs)
        # TODO: 记录出现异常的次数和日志
        logging.error("need to add ")