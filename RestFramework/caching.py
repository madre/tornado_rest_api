#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '2015/3/4'
__author__ = 'deling.ma'
"""
import hashlib
import json

from RestFramework import serializers
from RestFramework.redis_manager import RedisCache


class CacheMixin(object):
    def get_sql_cach(self, db_handle, sql, cache_time):
        # 查询并缓存结果，需要传入数据库句柄
        r = RedisCache.get_instance()
        sql_key = "zhuansql_" + hashlib.md5(sql).hexdigest()
        data_cache = r.get(sql_key)
        if not data_cache:
            db_handle.Q(sql)
            rs_obj = db_handle.fetchall()
            if not rs_obj:
                rs_obj = []
            r.set(sql_key, json.dumps(rs_obj, cls=serializers.JSONEncoder), cache_time)
            data_cache = r.get(sql_key)
        rs_obj = json.loads(data_cache)
        return rs_obj

    def check_cache(self, key):
        r = RedisCache.get_instance()
        rs = r.get(key)
        if rs:
            return rs
        return False

    def set_cache_obj(self, key, obj, ex):
        self.set_cache(key, json.dumps(obj), ex)

    def get_obj_cache(self, key):
        string = self.get_cache(key)
        if string:
            return json.loads(string)
        return None

    def set_cache(self, key, val, ex):
        r = RedisCache.get_instance()
        rs = r.set(key, val, ex)
        return True

    def get_cache(self, key):
        r = RedisCache.get_instance()
        rs = r.get(key)
        return rs

    def temp_cache_key(self, key):
        return "_ZHUAN_%s%s" % (self.__class__.__name__, key)
