# -*- coding: utf-8 -*-
import os

from sky.base import KmlMaker
from wea_foshan.base.data import DataManager
from config import ConfigL2


if __name__ == '__main__':
    if os.path.exists(ConfigL2.database_file):
        db = DataManager(database=ConfigL2.database_file)
        kml = KmlMaker()
        ct = 0

        for i in db.query_all_loc():
            kml.bulid_pm(i[1], i[2], i[3])
            ct += 1
        print(ct)
        kml.build_kml('1.kml')
