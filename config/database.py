# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  database.py
@Time    :  2023/4/24 11:55
@Author  :  Tangsj
@Version :  1.0
@Contact :  mqlwyz@163.com
@License :  (C)Copyright 2021-2022
@Desc    :  None
"""
from fb_modules.ModuleGetConfig import ReadConfigFile

def getmysqlconfig():
    config_ini = ReadConfigFile()
    result = config_ini.getSectionItem('MYSQL')
    # print(result.get("type"))
    return result