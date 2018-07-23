# -*- coding:utf-8 -*-
import time
from sqlalchemy import and_
from datetime import datetime

from sky.base import BaseORM

from wea_foshan.base.model import Address, Dat, Base
from wea_foshan.base.filectrl import attr, DataControl, open_data_file
from wea_foshan.base.ormtest import *

from config import ConfigL2

# 过滤函数
f = lambda x: None if not x else x

# 获取ORM基本操作
class DataManager(BaseORM, DataControl):

    def create_table(self):
        Base.metadata.create_all(self.engine)

    # ######
    # insert address
    # 插入单条站点地理数据
    def insert_address(self, name , eng_name=None, lng=None, lat=None, road=None, code=None):
        if self.get_address_id(name):
            print(r'插入[{}]数据失败,可能遇到重复数据.'.format(name))
            return None

        addr = Address(name=name, eng_name=eng_name, lng=lng, lat=lat, road=road, code=code)
        self.session.add(addr)
        print(r'插入[{}]站点成功.'.format(addr.name))
        return self.get_address_id(addr.name)

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


    # ######
    # get id
    def get_address_id(self, address_name):
        addr = self.session.query(Address).filter(Address.name == address_name).first()
        if not addr:
            return None
        return addr.id

    def get_address_name(self, address_id):
        addr = self.session.query(Address).filter(Address.name == address_id).first()
        if not addr:
            return None
        return addr.name

    def get_dat_id(self, logtime, address_id):
        dat = self.session.query(Dat).filter(and_(Dat.address_id==address_id, Dat.logtime==logtime)).first()
        if not dat:
            return None
        return dat.id


    # ######
    # insert dat
    # 插入单条站点气温数据
    def insert_dat(self, address_name, logtime, temp=None, rainfall=None, wdir=None, speed=None):
        # 检测站点有效性
        address_id = self.get_address_id(address_name)
        if not address_id:
            print('[{}]站点不存在.'.format(address_name))
            return None

        if self.get_dat_id(logtime, address_id):
            print(r'插入[{} {}]数据失败,可能遇到重复数据.'.format(logtime, address_name))
            return None

        dat = Dat(temp=temp, rainfall=rainfall, wdir=wdir, speed=speed, logtime=logtime, address_id=address_id)
        self.session.add(dat)
        print(r'插入[{} {}]数据成功.'.format(logtime, address_name))
        return self.get_dat_id(logtime, address_id)

    def insert_dat2(self, item, logtime):
        item = list(map(f, item))
        return self.insert_dat(item[attr.name],
                               logtime,
                               item[attr.temp],
                               item[attr.rainfall],
                               item[attr.wdir],
                               item[attr.speed])

    # 插入多条站点气温数据
    def insert_all_dat(self, data, logtime):
        if not data: return

        print('插入站点气温数据...')
        for i in data:
            if not self.get_dat_id(logtime, self.get_address_id(i[attr.name])):
                self.insert_dat2(i, logtime)
        print('插入完毕.')

    # ####
    # query loc
    # 查询指定id的地理数据
    def query_loc(self, address_id):
        addr = self.session.query(Address).filter(Address.id==address_id).first()
        if not addr:
            return None, None
        return addr.lng, addr.lat

    # 查询所有id的地理数据,包含id和name
    def query_all_loc(self):
        for i in self.session.query(Address).filter(Address.lng != None):
            yield i.id, i.name, i.lng, i.lat

    # ####
    # update loc
    # 更新地理信息
    def update_loc(self, address_id, lng, lat):
        loc = self.query_loc(address_id)        # 查询数据库原有信息
        if not loc[0] and lng:                  # 没有记录,并且有新信息则更新
            self.session.query(Address).filter(Address.id == address_id).update({'lng':lng, 'lat':lat})

    # 更新所有地理信息
    def update_all_loc(self, data):
        for i in data:
            self.update_loc(self.get_address_id(i[attr.name]), i[attr.lng], i[attr.lat])


    def update_from_file(self, file, reload=False):
        # 从数据文件名获取时间日期
        file_name = file.split('\\')[-1]
        logtime = datetime.strptime(file_name[:file_name.index('.')], '%Y%m%d_%H%M')

        # 数据存在则无需插入,启用reload选项强制重插
        if not reload:
            # 检查时间,已存在则返回
            res = self.session.query(Dat).filter(Dat.logtime == logtime.strftime('%Y-%m-%d %H:%M:%S')).first()
            if res:
                return

        data = open_data_file(file)
        self.insert_all_address(data)
        self.update_all_loc(data)
        self.insert_all_dat(data, logtime)


if __name__ == '__main__':
    # a = datetime.strptime('2018-07-11 00:00:00', '%Y-%m-%d %H:%M:%S')
    a = time.time()
    db = DataManager(SQLite3Test(ConfigL2.database_file).database, echo=False, autocommit=False)
    # db.create_table()
    # db.update_from_dir(debug_dir_cd2)

    print(db.get_address_id('禅城区张槎街道沙口水闸'))
    # print(db.get_address_id('禅城区张槎街道沙口水闸2'))
    # db.commit()
    b = time.time()
    print((b - a) * 1000)
    db.close()
