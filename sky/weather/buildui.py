# -*- coding: utf-8 -*-
import sys

from sky.ui.ui import Main

from PyQt4.QtCore import QTranslator
from PyQt4.QtGui import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    trans = QTranslator()
    trans.load("zh_CN")  # 没有后缀.qm
    app.installTranslator(trans)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())
