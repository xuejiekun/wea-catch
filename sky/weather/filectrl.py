# -*- coding: utf-8 -*-
import json
import os
from abc import ABCMeta,abstractmethod

from config import debug_dir


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
    with open(fileName, 'r', encoding='utf-8') as fp:
        try:
            data = json.loads(fp.read())
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
    debug_dir_cd2 = os.path.join('..', '..', debug_dir)

    if os.path.exists(debug_dir_cd2):
        file_list = get_all_file(debug_dir_cd2)
        print(file_list)

        data = open_data_file(file_list[0])
        show_data(data[:5])
