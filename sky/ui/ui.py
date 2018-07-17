# -*- coding:utf-8 -*-
import sys, time, os
from datetime import  datetime, timedelta

import sip
from PyQt4 import QtCore, QtGui

from sky.ui import  Ui_main, Ui_about
from sky.widget import ProgressBar
from sky.weather import FoshanCatch, FoshanData
from sky.weather.filectrl import get_all_file

from config import Config

class Main(QtGui.QMainWindow, Ui_main):
    barNum = 1

    def __init__(self, config):
        super().__init__()
        super().setupUi(self)
        self.set_signal_slot()
        self.init_widget()
        self.config = config

    # 初始化部分控件
    def init_widget(self):
        self.timer = QtCore.QBasicTimer()
        # self.timer.start(10, self)

    # 自定信号、槽
    def set_signal_slot(self):
        # 确定
        self.connect(self.btn_confirm, QtCore.SIGNAL("clicked()"), self.confirm)
        # 打开
        self.connect(self.btn_file, QtCore.SIGNAL("clicked()"), self.open)
        # 打开(菜单)
        self.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.open)
        # 关于(菜单)
        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.about)
        # 更新
        self.connect(self.btn_update, QtCore.SIGNAL("clicked()"), self.update_data)

    # 选取文件
    def open(self):

        file  = QtGui.QFileDialog(self).getOpenFileName(self, "选取文件", r".",
                                                        "All File (*);;Text File (*.txt);;Python File (*.py)")

        # file = QtGui.QFileDialog(self).getSaveFileName(self, "保存文件", r".",
        #                                                "All File (*);;Text File (*.txt);;Python File (*.py)")
        print(file)

        # directory = QtGui.QFileDialog(self).getExistingDirectory(self, "选取文件夹", r".")
        # print(directory)

    # 关于
    def about(self):
        self.ab = About()
        self.ab.show()

    # 更新
    def update_data(self):
        self.statusbar.showMessage('更新中...')
        print('更新中...')

        self.new_progressbar()
        print(self.config.debug_dir)
        self.update_task = UpdateTask(self.config, self.progressBar)
        self.update_task.progress_sign.connect(self.download_progress)
        self.update_task.close_sign.connect(self.close_progress)
        self.update_task.start()

    # 确定操作
    def confirm(self):
        # 获取日期
        date = self.calendarWidget.selectedDate().toPyDate()
        self.text_showdate.setText(str(date))
        self.statusbar.showMessage('选择了 {}'.format(str(date)))
        print('选择了 {}'.format(str(date)))

        self.new_progressbar()

        # 新建下载线程，并与进度条建立信号槽
        self.download_task = DownloadTask(self.config, self.progressBar, str(date))
        self.download_task.progress_sign.connect(self.download_progress)
        self.download_task.close_sign.connect(self.close_progress)
        self.download_task.start()

    def new_progressbar(self):
        # self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar = ProgressBar(self.centralwidget)
        self.gridLayout.addWidget(self.progressBar, self.barNum, 0, 1, 1)
        self.barNum += 1

    # 下载进度槽
    def download_progress(self, prog, num, prompt):
        prog.setValue(num)
        prog.setText(prompt)

    def close_progress(self, prog, prompt):
        self.gridLayout.removeWidget(prog)
        sip.delete(prog)
        self.barNum -= 1
        self.statusbar.showMessage(prompt)

    # 定时操作
    def timerEvent(self, event):
        pass


class About(QtGui.QDialog ,Ui_about):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.showDate()

    def showDate(self):
        pixmap = QtGui.QPixmap(":/img/out晒头.jpg")
        scaredPixmap = pixmap.scaled(120, 120, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaredPixmap)

        self.label_2.setText('Copyright by <b>Skywalker</b> , 2018')
        # self.label.setText('现在时间是:{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


class DownloadTask(QtCore.QThread):
    # 进度信号
    progress_sign = QtCore.pyqtSignal(QtGui.QProgressBar, int, str)
    close_sign = QtCore.pyqtSignal(QtGui.QProgressBar, str)

    def __init__(self, config, prog, date, date_format='%Y-%m-%d', ):
        super().__init__()
        self.prog = prog
        self.date = date
        self.date_format = date_format
        self.config = config

    def run(self):
        foshan = FoshanCatch()
        foshan.set_headers(self.config.user_agent)

        start = datetime.strptime(self.date, self.date_format)
        for i in range(24):
            code = foshan.download_time(self.config.debug_dir, start.strftime('%Y-%m-%d %H:%M:%S'), overwrite=self.config.overwrite)
            file_name = start.strftime('%Y%m%d_%H00') + r'.html'

            if code == FoshanCatch.expire:
                prompt = '{} 已过期.'.format(file_name)
            elif code == FoshanCatch.exist:
                prompt = '{} 已存在，不用下载.'.format(file_name)
            else:
                prompt = '下载 {}'.format(file_name)
            self.progress_sign.emit(self.prog, int((i+1)*100/24), prompt)

            start += timedelta(hours=1)
            time.sleep(0.4)

        self.close_sign.emit(self.prog, '{} 任务完成'.format(str(self.date)))


class UpdateTask(QtCore.QThread):
    progress_sign = QtCore.pyqtSignal(QtGui.QProgressBar, int, str)
    close_sign = QtCore.pyqtSignal(QtGui.QProgressBar, str)

    def __init__(self, config, prog):
        super().__init__()
        self.config = config
        self.prog = prog

    def run(self):
        foshan = FoshanData(database=self.config.database_file)
        file_list = get_all_file(self.config.debug_dir)

        all = len(file_list)
        index = 0
        for file in file_list:
            file_name = file.split('\\')[-1]
            self.progress_sign.emit(self.prog, int((index/all)*100), '读取 {}'.format(file_name))

            foshan.update_from_file(file, self.config.reload)
            index += 1
            self.progress_sign.emit(self.prog, int((index/all)*100), '从 {} 更新完毕'.format(file_name))

        self.close_sign.emit(self.prog, '数据更新完毕')
        foshan.close()


def run_gui(config):
    app = QtGui.QApplication(sys.argv)

    trans = QtCore.QTranslator()
    trans.load("zh_CN")  # 没有后缀.qm
    app.installTranslator(trans)

    ui = Main(config)
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    cf = Config(current=False)
    cf.set_overwrite(True)
    cf.set_reload(True)
    run_gui(cf)
