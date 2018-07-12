# -*- coding: utf-8 -*-
import  matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

class BasePlot:

    def __init__(self, size=(7,4)):
        self.fig, self.ax = plt.subplots(figsize=size)

    # 设置标题
    def set_label(self, xlab, ylab, title=''):
        self.ax.set_xlabel(xlab)
        self.ax.set_ylabel(ylab)
        self.ax.set_title(title)

    # 设置坐标范围
    def set_lim(self, xmin, xmax, ymin, ymax):
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)

    # 设置坐标轴标记位置(传递list)
    def set_tick(self, xtick, ytick):
        self.ax.set_xticks(xtick)
        self.ax.set_yticks(ytick)

    # 设置坐标轴标记位置(倍数)
    def set_tick_mul(self, xmajor=1, ymajor=1, xminor=0, yminor=0):
        self.ax.xaxis.set_major_locator(MultipleLocator(xmajor))
        self.ax.yaxis.set_major_locator(MultipleLocator(ymajor))
        self.ax.xaxis.set_minor_locator(MultipleLocator(xminor))
        self.ax.yaxis.set_minor_locator(MultipleLocator(yminor))

    # 设置坐标轴标记
    def set_xticklabel(self, xticklab):
        self.xticklab = xticklab
        self.ax.set_xticklabels(self.xticklab)

    def set_yticklabel(self, yticklab):
        self.yticklab = yticklab
        self.ax.set_yticklabels(self.yticklab)

    def shift_xtick(self, new_xticklab):
        self.xticklab.popleft()
        self.xticklab.append(new_xticklab)
        self.ax.set_xticklabels(self.xticklab)

    def shift_ytick(self, new_yticklab):
        self.yticklab.popleft()
        self.yticklab.append(new_yticklab)
        self.ax.set_xticklabels(self.yticklab)

    # x坐标轴刻度
    def set_xgrid(self, major_grid=False, minor_grid=False):
        self.ax.xaxis.grid(major_grid, which='major')
        self.ax.xaxis.grid(minor_grid, which='minor')

    # y坐标轴刻度
    def set_ygrid(self, major_grid=False, minor_grid=False):
        self.ax.yaxis.grid(major_grid, which='major')
        self.ax.yaxis.grid(minor_grid, which='minor')

    def set_grid(self, grid=False):
        self.ax.grid(grid)

    def plot(self, *args, **kwargs):
        self.ax.plot(*args, **kwargs)

    def show(self):
        plt.show()


if __name__ == '__main__':
    dr = BasePlot()
    dr.set_lim(0, 10, 0 ,20)
    dr.set_label('x100', 'y100', 'test')

    x = list(range(10))
    y = list(range(0, 20, 2))

    dr.plot(x, y)
    dr.show()
