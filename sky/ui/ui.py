# -*- coding:utf-8 -*-
import sys

import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTranslator
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QDialog
from datetime import  datetime

from sky.ui.mainui import  Ui_main
from sky.ui.aboutui import Ui_about


from sky.weather.catch import FoshanCatch
from config import user_agent, debug_dir_cd2

class Main(QMainWindow, Ui_main):
    i = 0
    upFlag = True

    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.set_signal_slot()
        self.set_timer()

    def set_timer(self):
        self.progressBar.setValue(0)
        self.timer = QtCore.QBasicTimer()
        self.timer.start(10, self)


    def set_signal_slot(self):
        self.connect(self.btn_confirm, QtCore.SIGNAL("clicked()"), self.confirm)
        self.connect(self.btn_file, QtCore.SIGNAL("clicked()"), self.open)
        self.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.open)
        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.about)

    def open(self):
        # directory = QFileDialog(self).getExistingDirectory(self, "选取文件夹", r".")
        file  = QFileDialog(self).getOpenFileName(self, "选取文件", r".", "All File (*);;Text File (*.txt);;Python File (*.py)")
        # file = QFileDialog(self).getSaveFileName(self, "保存文件", r".", "All File (*);;Text File (*.txt);;Python File (*.py)")
        print(file)
        # print(filetype)
        # print(directory)

    def about(self):
        self.sub = About()
        self.sub.text()
        self.sub.show()

    # 确定操作
    def confirm(self):
        date = self.calendarWidget.selectedDate().toPyDate()
        self.text_showdate.setText(str(date))
        self.statusbar.showMessage('选择了{}.'.format(str(date)))
        print(str(date))
        print(debug_dir_cd2)

        foshan= FoshanCatch()
        foshan.set_headers(user_agent)
        foshan.download_date(debug_dir_cd2, str(date))

    # 定时操作
    def timerEvent(self, event):
        if self.i < 100 and self.upFlag:self.i += 1
        else:self.i -= 1

        self.progressBar.setValue(self.i)
        # print(self.i)

        if self.i == 100:self.upFlag = False
        elif self.i == 0:self.upFlag = True


class About(QDialog ,Ui_about):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

    def text(self):
        self.label.setText(str(datetime.now()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    trans = QTranslator()
    trans.load("zh_CN")  # 没有后缀.qm
    app.installTranslator(trans)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())
