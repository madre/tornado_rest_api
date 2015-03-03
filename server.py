#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
import os
import platform
from tornado.ioloop import IOLoop
import tornado.httpserver
import tornado.web
from tornado.options import options as _options

from urls import application
import server_conf

if __name__ == "__main__":
    plat_str = platform.platform()
    if plat_str.startswith("Windows"):  # for windows
        print "start"
        server = tornado.httpserver.HTTPServer(application, xheaders=True)
        server.bind(8899)
        server.start()
        tornado.ioloop.IOLoop.instance().start()
    else:
        server = tornado.httpserver.HTTPServer(application, xheaders=True)
        server.bind(tornado.options.options.port)
        server.start(tornado.options.options.process)
        tornado.ioloop.IOLoop.instance().start()