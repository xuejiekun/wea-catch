# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName(_fromUtf8("main"))
        main.setWindowModality(QtCore.Qt.NonModal)
        main.setEnabled(True)
        main.resize(412, 350)
        main.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/huang.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(main)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.calendarWidget = QtGui.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.verticalLayout.addWidget(self.calendarWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.text_showdate = QtGui.QLineEdit(self.centralwidget)
        self.text_showdate.setObjectName(_fromUtf8("text_showdate"))
        self.horizontalLayout.addWidget(self.text_showdate)
        self.btn_confirm = QtGui.QPushButton(self.centralwidget)
        self.btn_confirm.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_confirm.setDefault(False)
        self.btn_confirm.setObjectName(_fromUtf8("btn_confirm"))
        self.horizontalLayout.addWidget(self.btn_confirm)
        self.btn_update = QtGui.QPushButton(self.centralwidget)
        self.btn_update.setObjectName(_fromUtf8("btn_update"))
        self.horizontalLayout.addWidget(self.btn_update)
        self.btn_file = QtGui.QPushButton(self.centralwidget)
        self.btn_file.setObjectName(_fromUtf8("btn_file"))
        self.horizontalLayout.addWidget(self.btn_file)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        main.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 412, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        main.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(main)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        main.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(main)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAbout = QtGui.QAction(main)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionOpen = QtGui.QAction(main)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/bird.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(main)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), main.close)
        QtCore.QMetaObject.connectSlotsByName(main)
        main.setTabOrder(self.btn_file, self.text_showdate)
        main.setTabOrder(self.text_showdate, self.btn_confirm)
        main.setTabOrder(self.btn_confirm, self.calendarWidget)
        main.setTabOrder(self.calendarWidget, self.btn_update)

    def retranslateUi(self, main):
        main.setWindowTitle(_translate("main", "demo", None))
        self.btn_confirm.setText(_translate("main", "confirm", None))
        self.btn_update.setText(_translate("main", "update", None))
        self.btn_file.setText(_translate("main", "open", None))
        self.menuFile.setTitle(_translate("main", "File", None))
        self.menuHelp.setTitle(_translate("main", "Help", None))
        self.actionExit.setText(_translate("main", "Exit", None))
        self.actionExit.setShortcut(_translate("main", "Ctrl+Q", None))
        self.actionAbout.setText(_translate("main", "About", None))
        self.actionOpen.setText(_translate("main", "Open", None))
        self.actionOpen.setShortcut(_translate("main", "Ctrl+O", None))

from . import img_rc
