# -*- coding: utf-8 -*-
import  matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pandas import Series, DataFrame
import numpy as np
import os

from sky.weather.data import FoshanData
from sky.datestr import *

from config import database_file


def get_mul(x, mul):
    if x % mul != 0:
        return x + (mul - x % mul)
    return x


# 获取数据
database_file = os.path.join('..', '..', database_file)
db = FoshanData(database_file)
start = '2018-06-10 00:00:00'
end = '2018-07-02 11:00:00'
address_id = 123
data = list(db.query_dat('temp', address_id, start, end, with_time=True))
print('数据长度:{}'.format(len(data)))

# 总时间
hours = total_hours(start,end)
print('总小时数:{}h'.format(hours+1))

# 期望表
exp = list()
t = start
hours = get_mul(hours, 24)
for i in range(hours+1):
    exp.append(t)
    t = get_end(t, hours=1)
# print(exp)

# 重新索引
s = list(zip(*data))
s = Series(s[1], index=s[0])
s = s.reindex(exp)
print(len(s))
# print(s.index)
# print(s.values)
print(s[s.isnull()])

# 绘图
fig, ax = plt.subplots(figsize=(9,5))
# s.plot(ax=ax)
# plt.show()

# 空df
df = DataFrame()
df['id'] = range(0,len(s))
df['temp']=s.values
df['datetime']=s.index
# print(df)

# 绘图
# df.plot(ax=ax, kind='scatter', x='id', y='temp', color='r')
ax.plot(df.temp.values)

ax.set_xlim(0, len(s)-1)
ax.set_ylim(22,36)
# ax.set_ylim(int(min(s.values)), int(max(s.values)+1))

f = lambda x:datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%m-%d')
exp = list(map(f, exp))
ax.set_xticks(np.arange(0, len(df), 24))
ax.set_xticklabels(exp[::24])
xminorLocator = MultipleLocator(6)
ax.xaxis.set_minor_locator(xminorLocator)

ax.set_xlabel('时间')
ax.set_ylabel('温度')

ax.set_yticks(np.arange(22, 37, 2))
# ax.set_yticks(np.arange(int(min(s.values)), int(max(s.values))+2, 2))

ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
ax.yaxis.grid(True, which='major') #y坐标轴的网格使用次刻度
ax.set_title('{} 至 {} \n{} 气温状况'.format(start, end, db.get_address_name(address_id)))
plt.show()
