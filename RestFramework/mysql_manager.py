# -*- coding: UTF-8 -*-
"""
mysql连接管理类
只能在tornado里面用

@author: zh
"""
import MySQLdb
import traceback
import logging

from tornado.options import options as _options
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class MysqlConn:
    executor = ThreadPoolExecutor(_options.db_max_process)
    db = None
    cur = None

    def __init__(self):
        if not self.db:
            self.db = MySQLdb.Connect(host=_options.db_host, user=_options.db_uname,
                                      passwd=_options.db_upass, port=int(_options.db_port),
                                      db=_options.db_name, charset="utf8")
            self.db.autocommit(True)
            self.cur = self.db.cursor()

    @staticmethod
    def F(sql):
        try:
            sql = MySQLdb.escape_string(sql)
            return sql
        except:
            print sql

    @run_on_executor
    def Q(self, sql):
        return self._query(sql)

    def TQ(self, sql):
        # 事物需要TQ支持 而不是Q
        rs = self.cur.execute(sql)
        return rs

    # 事物支持 , callback是个钩子
    @run_on_executor
    def worker(self, sql_list=None, callback=None):
        rs = False
        if not sql_list:
            return rs

        self.db.autocommit(False)
        try:
            for sql in sql_list:
                self.TQ(sql)

            self.db.commit()
            #放个钩子
            if callback:
                callback()

            rs = True
        except:
            traceback.print_exc()
            self.db.rollback()
            rs = False
        finally:
            self.db.autocommit(True)
        return rs

    def _query(self, sql):

        try:
            rs = self.cur.execute(sql)
            return rs
        except MySQLdb.Error, e:
            traceback.print_exc()
            logging.error("error: %s" % sql)

    def fetchone(self):
        return self.cur.fetchone()

    def fetchall(self):
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.db.close()
        self.db = None

    def __del__(self):
        try:
            if self.db is not None:
                self.close()
        except:
            pass

    def __exit__(self):
        try:
            if self.db is not None:
                self.close()
        except:
            pass