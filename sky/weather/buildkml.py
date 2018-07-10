# -*- coding: utf-8 -*-
import os

from sky.kml import KmlMaker
from sky.weather.data import FoshanData
from config import database_file


if __name__ == '__main__':
    # 数据库
    database_file = os.path.join('..', '..', database_file)
    db = FoshanData(database_file)
    kml = KmlMaker()
    ct = 0

    for i in db.query_all_loc():
        kml.bulid_pm(i[1], i[2], i[3])
        ct += 1
    print(ct)
    kml.build_kml('1.kml')
