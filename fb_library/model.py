# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  model.py
@Time    :  2023/4/24 14:33
@Author  :  Tangsj
@Version :  1.0
@Contact :  mqlwyz@163.com
@License :  (C)Copyright 2021-2022
@Desc    :  None
"""
from peewee import *
from fb_modules.ModuleGetConfig import ReadConfigFile
import datetime

# 加载配置文件到环境变量
config_ini = ReadConfigFile()
config = config_ini.getSectionItem('MYSQL')

sql_name   = config.get("type")
user       = config.get("username")
password   = config.get("password")
port       = int(config.get("hostport"))
host       = config.get("hostname")
prefix     = config.get("prefix")
charset    = config.get("charset")
debug      = config.get("debug")
database   = config.get("database")
"""
    如果是sqlite：那么使用 SqliteDatabase
    如果是mysql： 那么使用 MySQLDatabase
    如果是Postgresql： 那么使用 PostgresqlDatabase
"""
if not (host and port and user and
        password and database):
    raise Warning("conn_error, missing some params!")
db = MySQLDatabase(database, host=host, user=user, passwd=password, port=port)
# db = MySQLDatabase("street", host="127.0.0.1", user="root", passwd="root", port=3306)
# /Users/tangshijian/Service/UnityPy/venv_arm64/bin/python -c "import pymysql; conn = pymysql.connect(host='mysql_v2', user='root', password='123456', database='bg_client', port=3306); print(conn)"

class BaseModel(Model):
    class Meta:
        database = db

class Test(BaseModel):
    username = CharField(unique=True)

class Emote(Model):
    id      = AutoField(primary_key=True)
    name    = CharField()
    nameEN  = CharField()
    m_id    = CharField()
    img     = CharField()
    is_default     = IntegerField()
    is_animating   = IntegerField()
    guid    = CharField()
    prefab  = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        db_table = 'bg_emote'
        database = db

# if __name__=="__main__":
#     # Test.create_table()
#     # pass
#     # 连接数据库
#     database.connect()