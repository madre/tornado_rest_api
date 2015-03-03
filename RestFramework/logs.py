# -*- coding: utf-8  -*-
#!/usr/local/bin/python
"""
日志设置
__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""
import os
import logging
import logging.handlers

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def init_log():
    _LOG_PATH_ = os.path.join(BASE_DIR, "logs")
    if not os.path.isdir(_LOG_PATH_):
        os.makedirs(_LOG_PATH_)

    # access log，记录关键信息，按天分割，保留30天
    access_logger = logging.getLogger("api_access")
    access_log_file = os.path.join(_LOG_PATH_, "access.log")
    access_handler = logging.handlers.TimedRotatingFileHandler(access_log_file, when='midnight', backupCount=30)
    formatter = logging.Formatter("[%(asctime)s]: %(module)s %(levelname)s %(message)s ")
    access_handler.setFormatter(formatter)
    access_logger.addHandler(access_handler)
    access_logger.setLevel(logging.INFO)
    #access_logger.setLevel(logging.DEBUG)

    # error log，记录异常和错误信息，按天分割，保留30天
    error_logger = logging.getLogger("api_error")
    error_log_file = os.path.join(_LOG_PATH_, "error.log")
    error_handler = logging.handlers.TimedRotatingFileHandler(error_log_file, when='midnight', backupCount=30)
    formatter = logging.Formatter("[%(asctime)s]: %(module)s %(levelname)s %(message)s ")
    error_handler.setFormatter(formatter)
    error_logger.addHandler(error_handler)
    error_logger.setLevel(logging.ERROR)