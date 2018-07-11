# -*- coding:utf-8 -*-
import sys
import os
import time
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTranslator, pyqtSignal
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QDialog
from datetime import  datetime, timedelta

from sky.ui.mainui import  Ui_main
from sky.ui.aboutui import Ui_about

from sky.weather.catch import FoshanCatch
from config import user_agent, debug_dir_cd2

class Main(QMainWindow, Ui_main):
    barNum = 2

    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.set_signal_slot()
        self.init_widget()

    # 初始化部分控件
    def init_widget(self):
        self.progressBar.setValue(0)
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
        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.test)

    # 选取文件
    def open(self):

        file  = QFileDialog(self).getOpenFileName(self, "选取文件", r".",
                                                  "All File (*);;Text File (*.txt);;Python File (*.py)")

        # file = QFileDialog(self).getSaveFileName(self, "保存文件", r".",
        #                                          "All File (*);;Text File (*.txt);;Python File (*.py)")
        print(file)

        # directory = QFileDialog(self).getExistingDirectory(self, "选取文件夹", r".")
        # print(directory)

    # 关于
    def about(self):
        self.sub = About()
        self.sub.text()
        self.sub.show()

    def test(self):
        self.progressBar2 = QtGui.QProgressBar(self.centralwidget)
        self.progressBar2.setProperty("value", 0)
        self.progressBar2.statusTip()
        self.gridLayout.addWidget(self.progressBar2, self.barNum, 0, 1, 1)
        self.barNum += 1

    # 确定操作
    def confirm(self):
        # 获取日期
        date = self.calendarWidget.selectedDate().toPyDate()
        self.text_showdate.setText(str(date))
        self.statusbar.showMessage('选择了{}.'.format(str(date)))
        print('选择了{}.'.format(str(date)))

        # 新建下载线程，并与进度条建立信号槽
        self.download_task = DownloadTask(str(date))
        self.download_task.progress_sign.connect(self.download_progress)
        self.download_task.start()

    # 下载进度槽
    def download_progress(self, num, file_name):
        self.progressBar.setValue(num)
        self.statusbar.showMessage('下载 {}'.format(file_name))

    # 定时操作
    def timerEvent(self, event):
        pass


class About(QDialog ,Ui_about):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.text()

    def text(self):
        self.label.setText(str(datetime.now()))


class DownloadTask(QtCore.QThread):
    # 进度信号
    progress_sign = pyqtSignal(int, str)

    def __init__(self, date, date_format='%Y-%m-%d'):
        super().__init__()
        self.date = date
        self.date_format = date_format

    def run(self):
        foshan = FoshanCatch()
        foshan.set_headers(user_agent)

        start = datetime.strptime(self.date, self.date_format)
        for i in range(24):
            foshan.download_time(debug_dir_cd2, start.strftime('%Y-%m-%d %H:%M:%S'))
            file_name = start.strftime('%Y%m%d_%H00') + r'.html'
            self.progress_sign.emit(int((i+1)*100/24), file_name)
            start += timedelta(hours=1)
            time.sleep(2)

    # def run(self):
    #     for i in range(5):
    #         print('About: {}'.format(i))
    #         time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    trans = QTranslator()
    trans.load("zh_CN")  # 没有后缀.qm
    app.installTranslator(trans)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())
