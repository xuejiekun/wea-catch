# -*- coding:utf-8 -*-
from datetime import datetime, timedelta


# 获取结束时间字符串
def get_end(start, date_format='%Y-%m-%d %H:%M:%S', **kwargs):
    start_dt = datetime.strptime(start, date_format)
    return  (start_dt + timedelta(**kwargs)).strftime(date_format)


# 时间字符串格式转换
def change_format(datetime_str, old_format, new_format):
    return datetime.strptime(datetime_str, old_format).strftime(new_format)


# 返回两个时间字符串的小时差值
def total_hours(start, end, date_format='%Y-%m-%d %H:%M:%S'):
    start_dt = datetime.strptime(start, date_format)
    end_dt = datetime.strptime(end, date_format)
    return int((end_dt - start_dt).total_seconds() / 3600)

if __name__ == '__main__':
    start = '2018-06-12 12:00:00'
    end = get_end(start, days=-1)
    print(end)
    print(change_format(start, '%Y-%m-%d %H:%M:%S', '%Y%m%d_%H%M%S'))
    print(total_hours(start, end, '%Y-%m-%d %H:%M:%S'))
