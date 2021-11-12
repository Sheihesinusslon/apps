# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setAcceptDrops(True)
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.message_box = QPlainTextEdit(self.centralwidget)
        self.message_box.setObjectName(u"message_box")
        self.message_box.setFrameShape(QFrame.StyledPanel)
        self.message_box.setFrameShadow(QFrame.Sunken)
        self.message_box.setReadOnly(True)

        self.verticalLayout.addWidget(self.message_box)

        self.message_input = QLineEdit(self.centralwidget)
        self.message_input.setObjectName(u"message_input")

        self.verticalLayout.addWidget(self.message_input)

        self.button = QPushButton(self.centralwidget)
        self.button.setObjectName(u"button")

        self.verticalLayout.addWidget(self.button)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Messanger", None))
        self.message_box.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Connecting ...", None))
        self.message_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type message", None))
        self.button.setText(QCoreApplication.translate("MainWindow", u"Send", None))
    # retranslateUi

