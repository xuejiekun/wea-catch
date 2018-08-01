# -*- coding: utf-8 -*-
import os
import time

from sky.base.database import SQLite3
from sky.base.datestr import *

from wea_foshan.base.filectrl import attr, DataControl, open_data_file
from config import ConfigL2

# 过滤函数
f = lambda x: None if not x else x

class DataManager(SQLite3, DataControl):
    # ####
    # insert address
    # 插入单条站点地理数据
    def insert_address(self, name , eng_name, lng, lat, road, code):
        try:
            self.cursor.execute('insert into '
                                'address(name, eng_name, lng, lat, road, code) '
                                'values (?, ?, ?, ?, ?, ?)',
                                (name , eng_name, lng, lat, road, code))
        except:
            print(r'插入[{}]数据失败,可能遇到重复数据.'.format(name))
            return None

        print(r'插入[{}]站点成功.'.format(name))
        return self.get_address_id(name)

    # 插入单条站点地理数据2
    def insert_address2(self, item):
        item = list(map(f, item))
        return self.insert_address(item[attr.name],
                                   item[attr.eng_name],
                                   item[attr.lng],
                                   item[attr.lat],
                                   item[attr.road],
                                   item[attr.code])

    # 插入多条站点数据
    def insert_all_address(self, data):
        if not data: return

        print('插入站点地理数据...')
        for i in data:
            if not self.get_address_id(i[attr.name]):
                self.insert_address2(i)
        print('插入完毕.')


    # ####
    # get id
    def get_address_id(self, address_name):
        self.cursor.execute('select id from address where name=?', (address_name,))
        return self._return_one()

    def get_address_name(self, address_id):
        self.cursor.execute('select name from address where id=?', (address_id,))
        return self._return_one()

    def get_dat_id(self, logtime, address_id):
        self.cursor.execute('select id from dat '
                            'where logtime=? and address_id=?', (logtime, address_id))
        return self._return_one()


    # ####
    # insert dat
    # 插入单条站点气温数据
    def insert_dat(self, temp, rainfall, wdir, speed, logtime, address_name):
        # 检测站点名称
        address_id = self.get_address_id(address_name)
        if not address_id:
            print('[{}]站点不存在.'.format(address_name))
            return None

        try:
            self.cursor.execute('insert into '
                                'dat(temp, rainfall, wdir, speed, logtime, address_id) '
                                'values (?, ?, ?, ?, ?, ?)',
                                (temp, rainfall, wdir, speed, logtime, address_id))
        except:
            print(r'插入[{} {}]数据失败,可能遇到重复数据.'.format(logtime, address_name))
            return None

        print(r'插入[{} {}]数据成功.'.format(logtime, address_name))
        return self.get_dat_id(logtime, address_id)

    # 插入单条站点气温数据2
    def insert_dat2(self, item, logtime):
        item = list(map(f, item))
        return self.insert_dat(item[attr.temp],
                               item[attr.rainfall],
                               item[attr.wdir],
                               item[attr.speed],
                               logtime,
                               item[attr.name])

    # 插入多条站点气温数据
    def insert_all_dat(self, data, logtime):
        if not data: return

        print('插入站点气温数据...')
        for i in data:
            if not self.get_dat_id(logtime, self.get_address_id(i[attr.name])):
                self.insert_dat2(i, logtime)
        print('插入完毕.')

    # ####
    # query
    # 查询指定id的地理数据
    def query_loc(self, address_id):
        self.cursor.execute('select lng, lat from '
                            'address where id=?', (address_id, ))
        return self.cursor.fetchone()

    # 查询所以id的地理数据,包含id和name
    def query_all_loc(self):
        self.cursor.execute('select id, name, lng, lat from address where lng<>\'\'')
        for i in self.cursor:
            yield i

    # 更新地理信息
    def update_loc(self, address_id, lng, lat):
        # 查询数据库原有信息
        loc = self.query_loc(address_id)
        # 数据库没有记录并且有新信息
        if not loc[0] and lng:
            self.cursor.execute('update address '
                                'set lng=?, lat=?'
                                'where id=?',
                                (lng, lat, address_id))

    def update_all_loc(self, data):
        for i in data:
            self.update_loc(self.get_address_id(i[attr.name]), i[attr.lng], i[attr.lat])


    # 查询指定日期范围的数据内容
    def query_dat(self, content, address_id, start, end, date_format='%Y-%m-%d %H:%M:%S', with_time=False):
        # 将datetime string转换为合适的格式
        need_format = '%Y-%m-%d %H:%M:%S'
        start = change_format(start, date_format, need_format)
        end = change_format(end, date_format, need_format)

        self.cursor.execute('select logtime, {} from '
                            'dat inner join address '
                            'on dat.address_id=address.id '
                            'where address.id=? '
                            'and dat.logtime between ? and ?'.format(content),
                            (address_id, start, end))

        for i in self.cursor:
            if with_time:       # 包含时间的数据记录
                yield i
            else: yield i[1]    # 不包含时间的数据记录


    # 查询24小时的数据内容
    def query_dat_24(self, content, address_id, start, date_format='%Y-%m-%d %H:%M:%S'):
        end = get_end(start, date_format, days=1)
        return self.query_dat(content, address_id, start, end, date_format)


    # 从文件更新数据
    def update_from_file(self, file, reload=False):
        file_name = file.split('\\')[-1]
        logtime = datetime.strptime(file_name[:file_name.index('.')], '%Y%m%d_%H%M')

        # 数据存在则无需插入,启用reload强制重插
        if not reload:
            # 检查时间,已存在则返回
            self.cursor.execute('select logtime from dat '
                                'where datetime(logtime)=? limit 1',
                                (logtime.strftime('%Y-%m-%d %H:%M:%S'),))
            if self._return_one():
                return

        data = open_data_file(file)
        self.insert_all_address(data)
        self.update_all_loc(data)
        self.insert_all_dat(data, logtime)


if __name__ == '__main__':
    if os.path.exists(ConfigL2.database_file):
        db = DataManager(database=ConfigL2.database_file)
        i = []
        n = 1

        if n == 1:
            # 测试1 从文件更新数据
            file =  os.path.join(ConfigL2.debug_data_dir, '20180801', '20180801_0300.html')
            db.update_from_file(file)

        elif n == 2:
            # 测试2 从文件夹更新数据
            # data_dir = os.path.join(debug_dir, '20180618')
            a = time.time()
            db.update_from_dir(ConfigL2.debug_data_dir)
            b = time.time()
            print((b - a) * 1000)

        elif n == 3:
            # 测试3 查询指定范围的数据内容
            # i = wea_db.query_dat('rainfall', 35, '2018-06-12 12:00:00', '2018-06-14 12:00:00')
            i = db.query_dat('rainfall', 35, '2018061212', '2018061412', '%Y%m%d%H')

        elif n == 4:
            # 测试4查询24小时内的数据内容
            # i = wea_db.query_dat_24('rainfall', 35, '2018-06-12 12:00:00')
            i = db.query_dat_24('rainfall', 35, '2018061212', '%Y%m%d%H')

        i = list(i)
        print(i)
        print(len(i))

        db.close()
