# -*- coding: utf-8 -*-
import  matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


xmajorLocator = MultipleLocator(1)    #将x主刻度标签设置为20的倍数
xminorLocator = MultipleLocator(0.5)  #将x轴次刻度标签设置为5的倍数

ymajorLocator = MultipleLocator(5)    #将y轴主刻度标签设置为0.5的倍数
yminorLocator = MultipleLocator(1)    #将此y轴次刻度标签设置为0.1的倍数

class BasePlot:

    def __init__(self, size=(7,4)):
        self.fig, self.ax = plt.subplots(figsize=size)

    def set_lim(self, x_min, x_max, y_min, y_max, x_lab, y_lab, title):  # 设置坐标范围
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_xlabel(x_lab)
        self.ax.set_ylabel(y_lab)
        self.ax.set_title(title)

    def set_tick(self, x_tick, y_tick): # 设置坐标轴标记位置
        self.ax.set_xticks(x_tick)
        self.ax.set_yticks(y_tick)

    def set_tick2(self):    # 设置坐标轴标记位置(方法2)
        self.ax.xaxis.set_major_locator(xmajorLocator)
        self.ax.yaxis.set_major_locator(ymajorLocator)
        self.ax.xaxis.set_minor_locator(xminorLocator)
        self.ax.yaxis.set_minor_locator(yminorLocator)

    def set_ticklabel(self, x_ticklab):    # 设置坐标轴标记
        self.x_ticklab = x_ticklab
        self.ax.set_xticklabels(self.x_ticklab)

    def shift_xtick(self, new_ticklab):
        self.x_ticklab.popleft()
        self.x_ticklab.append(new_ticklab)
        self.ax.set_xticklabels(self.x_ticklab)

    def set_grid(self, grid=False):
        self.ax.grid(grid)

    def show(self):
        plt.show()
