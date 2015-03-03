#!/usr/bin/env python
# coding=utf-8
"""
基础工具集
__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""


def is_aware(value):
    """
    Determines if a given datetime.datetime is aware.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is not None and \
           value.tzinfo.utcoffset(value) is not None
