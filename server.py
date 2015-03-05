#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
import platform
from tornado.ioloop import IOLoop
import tornado.httpserver
import tornado.web
from tornado.options import options as _options

from RestFramework.log_config import init_log
import server_conf
# server.conf 需要在 application 之前调用
from applications import application

DAEMON = "zhuan_wifi_api"
try:
    import setproctitle
except ImportError:
    pass
else:
    setproctitle.setproctitle(DAEMON)


if __name__ == "__main__":
    plat_str = platform.platform()
    init_log()
    if plat_str.startswith("Windows"):  # for windows
        print "start"
        server = tornado.httpserver.HTTPServer(application, xheaders=True)
        server.bind(9819)
        server.start()
        tornado.ioloop.IOLoop.instance().start()
    else:
        server = tornado.httpserver.HTTPServer(application, xheaders=True)
        server.bind(tornado.options.options.port)
        server.start(tornado.options.options.process)
        tornado.ioloop.IOLoop.instance().start()