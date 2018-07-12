# -*- coding:utf-8 -*-
import sys, time, os
from datetime import  datetime, timedelta

import sip
from PyQt4 import QtCore, QtGui

from sky.ui import  Ui_main, Ui_about
from sky.widget import ProgressBar
from sky.weather import FoshanCatch

from config import user_agent, debug_dir_cd2

class Main(QtGui.QMainWindow, Ui_main):
    barNum = 1

    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.set_signal_slot()
        self.init_widget()

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

    # 确定操作
    def confirm(self):
        # 获取日期
        date = self.calendarWidget.selectedDate().toPyDate()
        self.text_showdate.setText(str(date))
        self.statusbar.showMessage('选择了 {}'.format(str(date)))
        print('选择了 {}'.format(str(date)))

        # self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar = ProgressBar(self.centralwidget)
        self.gridLayout.addWidget(self.progressBar, self.barNum, 0, 1, 1)
        self.barNum += 1

        # 新建下载线程，并与进度条建立信号槽
        self.download_task = DownloadTask(self.progressBar, str(date))
        self.download_task.progress_sign.connect(self.download_progress)
        self.download_task.close_sign.connect(self.close_progress)
        self.download_task.start()

    # 下载进度槽
    def download_progress(self, prog, num, prompt):
        prog.setValue(num)
        prog.setText(prompt)

    def close_progress(self, prog, date):
        self.gridLayout.removeWidget(prog)
        sip.delete(prog)
        self.statusbar.showMessage('{} 任务完成'.format(date))

    # 定时操作
    def timerEvent(self, event):
        pass


class About(QtGui.QDialog ,Ui_about):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.showDate()

    def showDate(self):
        pixmap = QtGui.QPixmap(r'F:\Project\Python\web_catch\wea\img\out晒头.jpg')
        scaredPixmap = pixmap.scaled(120, 120, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaredPixmap)

        self.label_2.setText('Copyright by <b>Skywalker</b> , 2018')
        # self.label.setText('现在时间是:{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


class DownloadTask(QtCore.QThread):
    # 进度信号
    progress_sign = QtCore.pyqtSignal(QtGui.QProgressBar, int, str)
    close_sign = QtCore.pyqtSignal(QtGui.QProgressBar, str)

    def __init__(self, prog, date, date_format='%Y-%m-%d'):
        super().__init__()
        self.prog = prog
        self.date = date
        self.date_format = date_format

    def run(self):
        foshan = FoshanCatch()
        foshan.set_headers(user_agent)

        start = datetime.strptime(self.date, self.date_format)
        for i in range(24):
            code = foshan.download_time(debug_dir_cd2, start.strftime('%Y-%m-%d %H:%M:%S'))
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

        self.close_sign.emit(self.prog, str(self.date))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    trans = QtCore.QTranslator()
    trans.load("zh_CN")  # 没有后缀.qm
    app.installTranslator(trans)

    ui = Main()
    ui.show()

    sys.exit(app.exec_())
