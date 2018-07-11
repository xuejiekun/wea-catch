# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtGui

class ProgressBar(QtGui.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUI()

    def setupUI(self):
        self.verticalLayout = QtGui.QVBoxLayout()
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setProperty("value", 0)

        self.label = QtGui.QLabel(self)

        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout.addWidget(self.label)
        self.setLayout(self.verticalLayout)

    def setText(self, string):
        self.label.setText(string)

    def setValue(self, num):
        self.progressBar.setValue(num)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = ProgressBar()
    ui.show()
    ui.setValue(40)
    ui.setText('ProgressBar')
    sys.exit(app.exec_())
