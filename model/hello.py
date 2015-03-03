#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
from RestFramework.handlers import RESTHandler


class HelloHandler(RESTHandler):
    AUTH_CHECK = True

    def get(self, *args, **kwargs):
        te = {"tes": "ew"}
        self.write(te)