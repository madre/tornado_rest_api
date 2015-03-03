#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
import os
import tornado.web
from model.hello import HelloHandler

_LOCAL_PATH_ = os.path.abspath(os.path.dirname(__file__))

settings = {
    "static_path": os.path.join(_LOCAL_PATH_, "html"),
    "template_path": os.path.join(_LOCAL_PATH_, "html"),
    "gzip": True,
    "debug": False
}

application = tornado.web.Application([
    (r"/hello", HelloHandler),
], **settings)
