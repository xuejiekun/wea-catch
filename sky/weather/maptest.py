# -*- coding: utf-8 -*-
import os

from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt

from sky.kml import KmlMaker
from sky.weather.data import FoshanData
from config import map_dir, map_dir_cpy, database_file


class PlotMap:

    def __init__(self):
        self.m = None
        self.ax = None

    def set_loc(self,lng, lat, length, width):
        self.lng = lng
        self.lat = lat
        self.length = length
        self.width = width

    def build_basemap(self, ax, resolution='h'):
        self.ax = ax
        self.m = Basemap(ax=self.ax,
                    projection='stere',
                    lon_0=self.lng, lat_0=self.lat,
                    llcrnrlon=self.lng - self.length/2,
                    urcrnrlon=self.lng + self.length/2,
                    llcrnrlat=self.lat - self.width/2,
                    urcrnrlat=self.lat + self.width/2,
                    resolution=resolution)

        self.m.drawcoastlines()
        self.m.drawcounties()
        self.m.drawstates()
        return self.m

    def get_basemap(self):
        return self.m

    def draw_bounds(self, name_loc, city_name):
        if not self.ax:
            print('还没有指定绘图地方.')
            return
        print(type(self.m.country_info))
        print(type(self.m.country))
        for info, side in zip(self.m.country_info, self.m.country):
            if info[name_loc] == city_name:
                poly = Polygon(side, facecolor='y', edgecolor='b', lw=1)
                self.ax.add_patch(poly)

    def read_shp(self, filename):
        if not self.m:
            return
        self.m.readshapefile(filename, 'country', drawbounds=False)

    def show(self):
        plt.show()


if __name__ == '__main__':
    # 数据库
    database_file = os.path.join('..', '..', database_file)
    db = FoshanData(database_file)

    # 绘图
    fig, ax = plt.subplots()
    # fig.tight_layout()
    m = PlotMap()
    m.set_loc(113, 23, 2, 1)

    map_file = os.path.join(map_dir, 'CHN_adm2')

    m.build_basemap(ax)
    m.read_shp(map_file)
    m.draw_bounds('NAME_2', 'Foshan')

    lng_list = []
    lat_list = []
    for i in db.query_all_loc():
        lng_list.append(i[2])
        lat_list.append(i[3])

    lng_list, lat_list = m.get_basemap()(lng_list, lat_list)

    ax.plot(lng_list, lat_list, 'b.')
    # m.build_basemap(axes[1])
    # m.read_shp(map_file)
    # m.draw_bounds('NAME_2', 'Guangzhou')
    m.show()
    db.close()


# lng_list = []
# lat_list = []
# for i in range(211):
#     loc = db.query_loc(i)
#     if loc and loc[0] != '':
#         lng_list.append(loc[0])
#         lat_list.append(loc[1])
# lng_list, lat_list = m(lng_list, lat_list)
# print(lng_list)
# print(lat_list)

# ax.plot(lng_list, lat_list, 'b.')
