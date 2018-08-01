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

    def get_data(self):
        before_one_hour = datetime.now()-timedelta(days=1)
        self.logger.info('download {}.html'.format(before_one_hour.strftime('%Y%m%d_%H00')))
        code = self.catch.download_time(self.data_dir, before_one_hour.strftime('%Y-%m-%d %H:00:00'))

        if code == WeaCatch.FINISH:
            self.logger.info('get data')

            file = os.path.join(self.data_dir,
                                before_one_hour.strftime('%Y%m%d'),
                                '{}.html'.format(before_one_hour.strftime('%Y%m%d_%H00')))
            db = DataManager(database=self.database)
            db.update_from_file(file)
            db.close()
        elif code == WeaCatch.EXIST:
            self.logger.info('exist')
        else:
            self.logger.info('not data')

    def test(self):
        self.logger.info('test')

    def run(self):
        self.logger.info('run')
        self.sched.add_job(self.get_data, 'cron', minute='41', misfire_grace_time=30)
        # self.sched.add_job(self.test, 'cron', second='0,10,20,30,40,50')
        self.sched.start()

    def stop(self):
        # self.db.close()
        self.sched.shutdown(wait=False)
