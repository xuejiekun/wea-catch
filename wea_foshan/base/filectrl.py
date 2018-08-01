# -*- coding: utf-8 -*-
import json
import os
from abc import ABCMeta,abstractmethod

from config import ConfigL2


class attr:
    name = 0
    temp = 1
    rainfall = 2
    wdir = 3
    speed = 4

    lng =5
    lat = 6
    road = 7
    eng_name = 8
    code = 9


class DataControl(metaclass=ABCMeta):
    @abstractmethod
    def update_from_file(self, file, reload=False):
        raise NotImplementedError

    def update_from_dir(self, data_dir, reload=False):
        file_list = get_all_file(data_dir)
        for file in file_list:
            self.update_from_file(file, reload=reload)


# 读取数据文件，返回list
def open_data_file(fileName):
    print('读取数据文件:{}'.format(fileName))
    with open(fileName, 'rb') as fp:
        try:
            data = json.loads(fp.read(), encoding='utf-8')
        except:
            print('数据文件格式不正确.')
            return []
        return data


# 递归读取数据文件夹,返回数据文件列表
def get_all_file(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


# 显示数据
def show_data(data):
    # title
    print(r'{:>5}   {:<5}{:<5}{:<}'.format('id', '气温', '时雨量', '站点'))

    # values
    ct = 0
    for i in data:
        print(r'{:>5}   {:<5}  {:<5}   {:<}'
              .format(ct+1, i[attr.temp], i[attr.rainfall], i[attr.name]))
        ct += 1
    print('共{}条记录.'.format(ct))


if __name__ == '__main__':
    if os.path.exists(ConfigL2.debug_data_dir):

        file_list = get_all_file(ConfigL2.debug_data_dir)
        print(file_list)

        data = open_data_file(file_list[0])
        # data = open_data_file(r'F:\Project\Python\web_catch\wea\res\debug_data\20180801\20180801_0300.html')
        show_data(data[:5])
