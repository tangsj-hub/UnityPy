# -*- coding: utf-8 -*-
# @Link    : https://github.com/aicezam/SmartOnmyoji
# @Version : Python3.7.6
# @MIT License Copyright (c) 2022 ACE

from configparser import ConfigParser
import configparser
from os.path import abspath, dirname, exists

#读取的相关方法：
# read(filename)：读取文件内容
#
# sections()：得到所有的section，并以列表的形式返回。
#
# options(section)：得到该section的所有option。
#
# items(section)：得到该section的所有键值对。
#
# get(section,option)：得到section中option的值，返回string类型。
#
# getint(section,option)：得到section中option的值，返回int类型。

# 写入的相关方法：
#
# write(fp)：将config对象写入至某个ini格式的文件中。
#
# add_section(section)：添加一个新的section。
#
# set(section,option,value)：对section中的option进行设置，需要调用write将内容写入配置文件。
#
# remove_section(section)：删除某个section。
#
# remove_option(section,option)：删除某个section下的option
class ReadConfigFile:
    def __init__(self):
        super(ReadConfigFile, self).__init__()
        self.file_path = abspath(dirname(dirname(__file__))) + r'/config.ini'  # 获取配置文件的绝对路径

    def getSectionItem(self, item = ''):
        config_ini = ConfigParser()

        # 校验文件是否存在
        if not exists(self.file_path):
            raise FileNotFoundError("配置文件不存在！")

        config_ini.read(self.file_path, encoding="utf-8-sig")  # 读配置文件

        # 读取confing.ini的参数
        result = dict(config_ini.items(item))
        if len(result) == 0:
            raise FileNotFoundError("配置文件下模块不存在！")
        else:
            #进行部分数据布尔类型的转化
            for i in result:
                # if i in ["run_endtime","power_num"]:
                #     result[i] = config_ini.getint(item, i)
                if (result[i] == 'True') | (result[i] == 'False'):
                    # result[i] = (result[i] == 'True') if True else False
                    result[i] = config_ini.getboolean(item, i)

        return result

    def writ_config(self, item, info):
        config_ini = configparser.RawConfigParser(comment_prefixes=('/'), allow_no_value=True)# 保留注释
        # config_ini = ConfigParser(comment_prefixes=('/'), allow_no_value=True)  # 保留注释
        # 校验文件是否存在
        if not exists(self.file_path):
            raise FileNotFoundError("配置文件不存在！")

        config_ini.read(self.file_path, encoding="utf-8-sig")  # 读配置文件
        for i in info:
            config_ini.set(item, i, info[i])

        # 写入文件
        config_ini.write(open(self.file_path, 'w', encoding="utf-8"))
