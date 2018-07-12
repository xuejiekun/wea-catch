# -*- coding: utf-8 -*-
import os

from sky.base import BasePlot
from sky.base.datestr import *
from sky.weather.data import FoshanData

from config import database_file_cd2


class WeatherPlot(BasePlot):

    def __init__(self, size=(7,4)):
        super().__init__(size)

    def plot(self, data, content, address_name, start, date_format='%Y-%m-%d %H:%M:%S', plot_format='plot', grid=False):
        # 获取终止时间的字符串
        hours = len(data)
        end = get_end(start, date_format, hours=hours-1)
        # 转换格式
        need_format = '%Y-%m-%d %H:%M:%S'
        start = change_format(start, date_format, need_format)
        end = change_format(end, date_format, need_format)

        # 设置标题和值域
        label = ''
        if content=='rainfall':
            self.set_lim(-1, hours,
                         0, round(max(data)+1))
            self.set_label('时间', '时雨量(mm)',
                           '{} 至 {} \n{} 降雨状况'.format(start, end, address_name))
            self.set_tick(range(hours),
                          range(0, round(max(data) + 2), 2))
            label = '累积雨量:{}mm'.format(round(sum(data), 0))

        elif content=='temp':
            self.set_lim(0, hours-1,
                         round(min(data)-1), round(max(data)+1))
            self.set_label('时间', '气温(℃)',
                           '{} 至 {} \n{} 气温状况'.format(start, end, address_name))
            self.set_tick(range(hours),
                          range(round(min(data)-1), round(max(data)+2), 1))
            label = '最高温度:{}℃'.format(max(data), 0)

        # 设置x轴标记
        x_ticklable = []
        if hours < 50:
            base = datetime.strptime(start, need_format).hour
            for i in range(hours):
                x_ticklable.append(base + i)
                if base + i == 23:
                    base += -24
        else:
            self.ax.set_xticks([])
            grid = False
        self.set_xticklabel(x_ticklable)

        if plot_format=='bar':
            self.ax.bar(range(0, hours), data)
        elif plot_format=='plot':
            self.ax.plot(data)

        self.ax.legend(labels=[label])
        self.set_grid(grid)
        self.show()

    def plot_rainfall(self, data, address_name, start, date_format='%Y-%m-%d %H:%M:%S'):
        self.plot(data, 'rainfall', address_name, start, date_format, 'bar')

    def plot_temp(self, data, address_name, start, date_format='%Y-%m-%d %H:%M:%S'):
        self.plot(data, 'temp', address_name, start, date_format, grid=True)


if __name__ == '__main__':
    if os.path.exists(database_file_cd2):

        wea_db = FoshanData(database=database_file_cd2)
        wea_plt = WeatherPlot()

        start = '2018-06-12 16:00:00'
        end = '2018-06-14 16:00:00'
        address_id = 35
        address_name = wea_db.get_address_name(address_id)

        data = list(wea_db.query_dat('rainfall', address_id, start, end))
        wea_plt.plot_rainfall(data, address_name, start)

        # data = list(wea_db.query_dat_24('temp', address_id, start))
        # wea_plt.plot_temp(data, address_name, start)

        wea_db.close()
