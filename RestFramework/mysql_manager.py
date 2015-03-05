# -*- coding: UTF-8 -*-
"""
mysql连接管理类
只能在tornado里面用

主要目标：
带读写分离，带多读库支持

次要目标：
带任何条件下数据库异步

@author: zh
"""
import MySQLdb
import traceback
import logging
from tornado.options import define, options as _options
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class MysqlConn:
    executor = ThreadPoolExecutor(_options.db_max_process)
    db = None
    cur = None
    default_db_name = ""

    def __init__(self, db_name=""):
        self.get_conn(db_name)

    def get_conn(self, db_name=""):
        if self.db is None:
            # 主库 读写
            if db_name == "":
                self.db = MySQLdb.Connect(host=_options.db_host, user=_options.db_uname,
                                          passwd=_options.db_upass, port=int(_options.db_port),
                                          db=_options.db_name, charset="utf8")
                self.db.autocommit(True)
                self.cur = self.db.cursor()
            # 其他各种库
            if db_name != "":
                self.db = MySQLdb.Connect(host=getattr(_options, "db_" + db_name + "_host"),
                                          user=getattr(_options, "db_" + db_name + "_uname"),
                                          passwd=getattr(_options, "db_" + db_name + "_upass"),
                                          port=int(getattr(_options, "db_" + db_name + "_port")),
                                          db=getattr(_options, "db_" + db_name + "_name"), charset="utf8")
                self.db.autocommit(True)
                self.cur = self.db.cursor()
            # 消息积分库 读写
            #             if db_name=="d":
            #                 self.db = MySQLdb.Connect(host=_options.db_d_host ,user=_options.db_d_uname ,
            #                              passwd=_options.db_d_upass ,port=int(_options.db_d_port) ,
            #                              db=_options.db_d_name ,charset="utf8" )
            #                 self.db.autocommit(True)
            #                 self.cur=self.db.cursor()

    # filter
    @staticmethod
    def F(sql):
        try:
            sql = MySQLdb.escape_string(sql)
            return sql
        except:
            print sql

    # 异步方式请求数据库
    @run_on_executor
    def SQ(self, sql):
        return self._query(sql)

    # 普通方式请求数据库
    def Q(self, sql):
        return self._query(sql)

    def TQ(self, sql):
        # 事物需要TQ支持 而不是Q
        rs = self.cur.execute(sql)
        return rs

    # 事物支持, callback是个钩子
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
            # 放个钩子
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
        try:
            self.cur.close()
        except:
            pass
        try:
            self.db.close()
        except:
            pass
            self.db = None

    def __del__(self):
        try:
            if self.db != None:
                self.close()
        except:
            pass

    def __exit__(self):
        # 添加对with语句的支持
        try:
            if self.db != None:
                self.close()
        except:
            pass
