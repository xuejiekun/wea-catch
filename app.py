# -*- coding: utf-8 -*-
import argparse
import time

from sky.base.datestr import *

from wea_foshan.base import DataManager, WeaCatch
from wea_foshan.base.plot import WeaPlot
from config import Config


def update(start=None, end=None, date_format='%Y-%m-%d %H:%M:%S', yesterday=False, overwrite=False, reload=False):
    catch = WeaCatch()

    if not start and not end:
        catch.download_today(Config.debug_data_dir, yesterday, overwrite)
    elif start and not end:
        catch.download_time(Config.debug_data_dir, start, date_format, overwrite)
    elif start and end:
        catch.download_data(Config.debug_data_dir, start, end, date_format, overwrite)

    db = DataManager(database=Config.database_file)
    db.update_from_dir(Config.debug_data_dir, reload)
    db.close()


def plot(content, address_id, start, end=None, date_format='%Y-%m-%d %H:%M:%S'):
    db = DataManager(database=Config.database_file)
    wea_plt = WeaPlot()
    address_name = db.get_address_name(address_id)

    if end:
        data = list(db.query_dat(content, address_id, start, end, date_format))
    else:
        data = list(db.query_dat_24(content, address_id, start, date_format))

    if content=='rainfall':
        wea_plt.plot_rainfall(data, address_name, start, date_format)
    elif content=='temp':
        wea_plt.plot_temp(data, address_name, start, date_format)

    db.close()


if __name__ == '__main__':
    # plot('temp', 7, '2018-06-17 23:00:00')
    # plot('rainfall', 35, '2018061216', date_format='%Y%m%d%H')

    # a = time.time()
    # update()
    # b = time.time()
    # print((b-a)*1000)

    choices = ('update', 'plot')

    parser = argparse.ArgumentParser(description='update or plot from the weather database')
    parser.add_argument('action', choices=choices, help='what do you want to do')
    parser.add_argument('--id', metavar='address-id', type=int, help='')
    parser.add_argument('-s', dest='start', metavar='start-time',  type=str, help='')
    parser.add_argument('-e', dest='end', metavar='end-time', type=str, help='')
    parser.add_argument('-c', dest='content', metavar='content', type=str, help='')
    parser.add_argument('-f', dest='overwrite', action='store_true', default=False, help='')
    parser.add_argument('-y', dest='yesterday', action='store_true', default=False, help='')
    parser.add_argument('-r', dest='reload', action='store_true', default=False, help='')

    args = parser.parse_args()

    if args.action == 'plot':
        # 只有start参数
        if args.content and args.id and args.start and not args.end:
            if args.yesterday:
                args.start = get_end(args.start, '%Y%m%d%H', days=-1)
                plot(args.content, args.id, args.start, date_format='%Y%m%d%H')
            else:
                plot(args.content, args.id, args.start, date_format='%Y%m%d%H')
        # 既有start又有end
        elif args.content and args.id and args.start and args.end:
            plot(args.content, args.id, args.start, args.end, '%Y%m%d%H')
        # 参数不完整
        else:
            print('运行plot需要:--id -s [-e] -c 参数')


    elif args.action == 'update':
        # 没有参数
        if not args.start and not args.end:
            update(yesterday=args.yesterday, overwrite=args.overwrite, reload=args.reload)
        # 只有start参数
        elif args.start and not args.end:
            update(args.start, date_format='%Y%m%d%H', overwrite=args.overwrite, reload=args.reload)
        # 既有start又有end
        elif args.start and args.end:
            update(args.start, args.end, '%Y%m%d%H', overwrite=args.overwrite, reload=args.reload)
        else:
            print('需要-s 参数与-e 参数配合使用')
