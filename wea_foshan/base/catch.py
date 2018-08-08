# -*- coding: utf-8 -*-
import os
import time
import numpy as np
from datetime import datetime, timedelta

from sky.base import BaseRequests, change_format, total_hours
from config import ConfigL2


class WeaCatch(BaseRequests):
    FINISH = 0
    EXIST = 1
    EXPIRE= 2
    NOTFOUND = 4

    home_url = r'http://www.fs121.gov.cn'
    home_url2 = r'http://www.fs121.com/wap/Awshour.aspx#sid=6'

    # 获取数据地址
    @staticmethod
    def data_url(date, date_format='%Y-%m-%d %H:%M:%S'):
        date = change_format(date, date_format, '%Y%m%d-%H00')
        return r'http://www.fs121.com/Awshour/dat/' \
               r'TQList-{}.js?t={}'.format(date, np.random.rand())


    def __init__(self, delay=2, timeout=5):
        super().__init__()
        self.delay = delay
        self.timeout = timeout


    # 下载指定时间的数据
    def download_time(self, data_dir, date, date_format='%Y-%m-%d %H:%M:%S', overwrite=False):
        start = datetime.strptime(date, date_format)

        # 设置下载目录(eg.data_dir/20180606/)
        down_dir = os.path.join(data_dir, start.strftime('%Y%m%d'))
        if not os.path.exists(down_dir):
            os.makedirs(down_dir, exist_ok=True)

        # 设置文件名(eg.20180606_1500.html)
        file_name = start.strftime('%Y%m%d_%H00') + r'.html'
        file = os.path.join(down_dir, file_name)

        if os.path.exists(file) and not overwrite:
            print('[{}]数据文件已存在，不用下载.'.format(file_name))
            return self.EXIST

        # 请求下载地址
        while not self.get_page(self.data_url(start.strftime('%Y-%m-%d %H:%M:%S')), timeout=self.timeout):
            print('请求超时，等待{}s重连'.format(self.timeout))
            time.sleep(self.timeout)

        # 保存数据
        if self.response.url == r'http://www.fs121.com/':
            print('请求的[{}]数据已过期.'.format(file_name))
            return self.EXPIRE

        if self.response.status_code == 404:
            print('[{}] 找不到.'.format(file_name))
            return self.NOTFOUND

        self.save_as_html(file)
        print('下载完毕:{}'.format(self.response.url))
        return self.FINISH


    # 下载指定日期的数据
    def download_date(self, data_dir, date, date_format='%Y-%m-%d', overwrite=False):
        start = datetime.strptime(date, date_format)

        # 先请求主页获取cookies
        self.get_page(self.home_url)
        for i in range(24):
            code = self.download_time(data_dir, start.strftime('%Y-%m-%d %H:%M:%S'), overwrite=overwrite)
            start += timedelta(hours=1)
            if code == self.FINISH:
                time.sleep(self.delay)


    # 下载指定范围的数据
    def download_data(self, data_dir, start, end, date_format='%Y-%m-%d %H:%M:%S', overwrite=False):
        # 转为需要的格式(eg.'2018-06-06 15:00:00'), 并获取小时差(闭区间)
        need_format = '%Y-%m-%d %H:00:00'
        start_dt = datetime.strptime(change_format(start, date_format, need_format), need_format)
        hours = total_hours(start, end, date_format) + 1

        # 先请求主页获取cookies
        self.get_page(self.home_url)
        for i in range(hours):
            self.download_time(data_dir, start_dt.strftime('%Y-%m-%d %H:%M:%S'), overwrite=overwrite)
            start_dt += timedelta(hours=1)
            time.sleep(self.delay)


    # 下载今天(昨天)的数据
    def download_today(self, data_dir, yesterday=False, overwrite=False):
        if yesterday:
            yesterday = datetime.now()-timedelta(days=1)
            self.download_date(data_dir, yesterday.strftime('%Y-%m-%d'), overwrite=overwrite)
        else:
            today = datetime.now()
            start = today.strftime('%Y-%m-%d 00:%M:%S')
            end = today.strftime('%Y-%m-%d %H:%M:%S')
            self.download_data(data_dir, start, end, overwrite=overwrite)


if __name__ == '__main__':
    if os.path.exists(ConfigL2.debug_data_dir):

        catch = WeaCatch()
        catch.set_headers(ConfigL2.user_agent)
        n = 2

        if n==1:
            # 测试1 下载指定范围
            catch.download_data(ConfigL2.debug_data_dir, '2018-06-17 23:10:00', '2018-06-18 06:44:00')
            # foshan.download_data(debug_dir, '2018061723', '2018061806', '%Y%m%d%H')

        elif n==2:
            # 测试2 下载指定小时
            catch.download_time(ConfigL2.debug_data_dir, '2018-08-01 00:10:00')
            # foshan.download_hour(debug_dir, '2018061723', '%Y%m%d%H')

        elif n==3:
            # 测试3 下载指定日期
            # foshan.download_today(debug_dir)
            catch.download_date(ConfigL2.debug_data_dir, '2018-07-07')
