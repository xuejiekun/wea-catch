# -*- coding:utf-8 -*-
import inspect
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

from wea_foshan.base import WeaCatch, DataManager


class Task:
    def __init__(self, logger):
        self.logger = logger
        self.sched = BlockingScheduler()
        self.catch = WeaCatch()

        self.current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        self.data_dir = os.path.join(self.current_dir, 'res/debug_data')
        self.database = os.path.join(self.current_dir, 'data.db')
        # self.db = DataManager(database=self.database)

    # 下载前一小时的数据
    def get_data(self):
        before_one_hour = datetime.now()-timedelta(hours=1)
        file_name = '{}.html'.format(before_one_hour.strftime('%Y%m%d_%H00'))
        self.logger.info('download {}'.format(file_name))

        code = self.catch.download_time(self.data_dir, before_one_hour.strftime('%Y-%m-%d %H:00:00'))

        # FINISH
        if code == WeaCatch.FINISH:
            self.logger.info('get data')

            file_name_abs = os.path.join(self.data_dir, before_one_hour.strftime('%Y%m%d'), file_name)
            db = DataManager(database=self.database)
            db.update_from_file(file_name_abs)
            db.close()
        # EXIST
        elif code == WeaCatch.EXIST:
            self.logger.info('exist')
        # NOT
        else:
            self.logger.info('not data')

    def test(self):
        self.logger.info('test')

    def run(self):
        self.logger.info('run')
        self.sched.add_job(self.get_data, 'cron', minute='45', misfire_grace_time=30)
        # self.sched.add_job(self.test, 'cron', second='0,10,20,30,40,50')
        self.sched.start()

    def stop(self):
        # self.db.close()
        self.sched.shutdown(wait=False)
