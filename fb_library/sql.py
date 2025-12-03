# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  sql.py
@Time    :  2023/4/24 11:58
@Author  :  Tangsj
@Version :  1.0
@Contact :  mqlwyz@163.com
@License :  (C)Copyright 2021-2022
@Desc    :  None
"""
# -*- coding:utf-8 -*-
# import psycopg2
import pymysql
import os
from fb_modules.ModuleGetConfig import ReadConfigFile
# import pymssql
# import cx_Oracle


import time
from functools import wraps
from contextlib import contextmanager


# 测试一个函数的运行时间，使用方式：在待测函数直接添加此修饰器
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('\n============================================================')
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        print('============================================================\n')
        return r
    return wrapper


# 测试一段代码运行的时间，使用方式：上下文管理器with
# with timeblock('block_name'):
#     your_code_block...
@contextmanager
def timeblock(label='Code'):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print('==============================================================')
        print('{} run time: {}'.format(label, end - start))
        print('==============================================================')


class SqlConn():
    '''
    连接数据库，以及进行一些操作的封装
    '''
    # sql_name = ''
    # database = ''
    # user = ''
    # password = ''
    # port = 0
    # host = ''

    # 创建连接、游标
    def __init__(self):
        # 加载配置文件到环境变量
        config_ini = ReadConfigFile()
        config = config_ini.getSectionItem('MYSQL')

        self.sql_name   = config.get("type")
        self.user       = config.get("username")
        self.password   = config.get("password")
        self.port       = int(config.get("hostport"))
        self.host       = config.get("hostname")
        self.prefix     = config.get("prefix")
        self.charset    = config.get("charset")
        self.debug      = config.get("debug")
        self.database   = config.get("database")
        # self.tablename   = self.prefix + config.get("database") if self.prefix else config.get("database")

        # print(self.sql_name,self.database,self.user,self.password,self.port,self.host)
        # exit()

        if not (self.host and self.port and self.user and
                self.password and self.database):
            raise Warning("conn_error, missing some params!")

        # sql_conn = {'mysql': pymysql,
        #             'postgresql': psycopg2,
        #             'sqlserver': pymssql,
        #             'orcle': cx_Oracle
        #             }
        sql_conn = {'mysql': pymysql}

        self.conn = sql_conn[self.sql_name].connect(host=self.host,
                                                    port=self.port,
                                                    user=self.user,
                                                    password=self.password,
                                                    database=self.database,
                                                    )
        #创建游标：（我们需要用游标来执行各种操作）
        self.cursor = self.conn.cursor()
        if not self.cursor:
            raise Warning("conn_error!")

    # 测试连接
    def test_conn(self):
        if self.cursor:
            print("conn success!")
        else:
            print('conn error!')

    # 单条语句的并提交
    def execute(self, sql_code):
        self.cursor.execute(sql_code)
        self.conn.commit()

    # 单条语句的不提交
    def execute_no_conmmit(self, sql_code):
        self.cursor.execute(sql_code)

    # 构造多条语句，使用%s参数化，对于每个list都进行替代构造
    def excute_many(self, sql_base, param_list):
        self.cursor.executemany(sql_base, param_list)

    # 批量执行（待完善）
    def batch_execute(self, sql_code):
        pass

    # 获取数据
    def get_data(self, sql_code, count=0):
        self.cursor.execute(sql_code)
        if int(count):
            return self.cursor.fetchmany(count)
        else:
            return self.cursor.fetchall()

    def get_count(self, sql_code):
        try:
            # 执行 SQL 查询
            self.cursor.execute(sql_code)
            
            # 获取查询结果的数量
            result_count = self.cursor.rowcount
            
            # 返回查询结果的数量
            return result_count
        
        except Exception as e:
            print(f"Error executing SQL: {e}")
            return None  
    # 更新数据
    def update(self, sql_code):
        self.cursor.execute(sql_code)

    # 插入数据
    def insert(self, sql_code):
        self.cursor.execute(sql_code)

    # 滚动游标
    def cursor_scroll(self, count, mode='relative'):
        self.cursor.scroll(count, mode=mode)

    # 提交
    def commit(self):
        self.conn.commit()

    # 回滚
    def rollback(self):
        self.conn.rollback()

    # 关闭连接
    def close_conn(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    SqlConn = SqlConn()
    SqlConn.test_conn()
