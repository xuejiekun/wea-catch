# -*- coding:utf-8 -*-
import os

# 测试header
test_url = r'https://www.whatismybrowser.com/'

#
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
             r'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             r'Chrome/63.0.3239.132 Safari/537.36'

# 数据源目录
data_dir = r'data'

# 数据源(测试)目录
debug_dir = r'debug_data'
debug_dir_cd2 = os.path.join('..', '..', debug_dir)

# sqlite3数据库文件
database_file = r'data.db'
database_file_cd2 = os.path.join('..', '..', database_file)

# shp地图包
map_dir = r'F:\Project\Python\CHN_adm_shp'

# shp地图包(公司)
map_dir_cpy = r'H:\Python\CHN_adm_shp'

class Config:
    def __init__(self, current=True):
        self.user_agent = user_agent
        self.overwrite = False
        self.reload = False

        if current:
            self.debug_dir = debug_dir
            self.database_file = database_file
        else:
            self.debug_dir = debug_dir_cd2
            self.database_file = database_file_cd2

    def set_overwrite(self, overwrite):
        self.overwrite = overwrite

    def set_reload(self, reload):
        self.reload = reload
