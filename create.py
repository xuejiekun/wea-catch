# -*- coding:utf-8 -*-
from sky.weather.dataorm import FoshanData

db = FoshanData('sqlite:///data.db')
db.create_table()
db.close()
