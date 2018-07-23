# -*- coding:utf-8 -*-
from wea_foshan.base.dataorm import DataManager

db = DataManager('sqlite:///data.db')
db.create_table()
db.close()
