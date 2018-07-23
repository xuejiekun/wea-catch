# -*- coding:utf-8 -*-
import os


class Config:
    # 测试header
    test_url = r'https://www.whatismybrowser.com/'

    user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
                 r'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 r'Chrome/63.0.3239.132 Safari/537.36'

    # 数据源目录
    data_dir = r'res/data'

    # 数据源(测试)目录
    debug_data_dir = r'res/debug_data'

    #sqlite3数据库文件
    database_file = r'data.db'

    # shp地图包
    map_dir = r'F:\Project\Python\CHN_adm_shp'

    # shp地图包(公司)
    map_dir_cpy = r'H:\Python\CHN_adm_shp'

    def set_overwrite(self, overwrite):
        self.overwrite = overwrite

    def set_reload(self, reload):
        self.reload = reload


class ConfigL1(Config):
    data_dir = r'../res/data'
    debug_data_dir = r'../res/debug_data'
    database_file = r'../data.db'


class ConfigL2(Config):
    data_dir = r'../../res/data'
    debug_data_dir = r'../../res/debug_data'
    database_file = r'../../data.db'
