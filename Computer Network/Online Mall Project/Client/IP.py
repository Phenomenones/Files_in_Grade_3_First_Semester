# -*- coding: utf-8 -*-
import pyDes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
import sys
import os
import time

HOST = '127.0.0.1'  #连接的IP地址
PORT = 65432    #发送端口号
HEADIMAGE_PORT = 65431  #登记新用户时发送头像的端口
BUFFERSIZE=1048576  #缓冲区大小
KEY=b"i*k&y^t%" #DES加密的秘钥
TIMEOUT = 5
RECEIVE_PORT = 23333    #另一个线程接收弹窗的端口的起始
CURRENT_HOST = '0.0.0.0'

def encrypt(string):    #加密函数
    k = pyDes.des(KEY, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    return k.encrypt(string)

def decrypt(string):    #解密函数
    k = pyDes.des(KEY, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    return k.decrypt(string)

def get_time_stamp():   #时间戳，防止重放攻击
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    timestamp = time.mktime(time_local)
    return timestamp
    
class Error_Dialog(QDialog):    #提示错误窗口
    def __init__(self,parent=None):
        super(Error_Dialog,self).__init__(parent)
        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(340, 110)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 290, 66))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.TipLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.TipLabel.setObjectName("TipLabel")
        self.horizontalLayout.addWidget(self.TipLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.EnsureButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.EnsureButton.setObjectName("EnsureButton")
        self.EnsureButton.setIcon(QtGui.QIcon('icon/confirm.ico'))
        self.EnsureButton.clicked.connect(self.close_)
        self.horizontalLayout_2.addWidget(self.EnsureButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Error!"))
        self.TipLabel.setText(_translate("Dialog", "Operation Failed!"))
        self.EnsureButton.setText(_translate("Dialog", "OK"))

        file = QtCore.QFile('black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()
    
    def close_(self):
        self.hide()

    def show_myself(self):
        self.show()


class MessageBox_Dialog(QDialog):
    def __init__(self,parent=None):
        super(MessageBox_Dialog,self).__init__(parent)
        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(380, 320)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 20, 300, 280))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.FromIDLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.FromIDLine.setObjectName("FromIDLine")
        self.FromIDLine.setReadOnly(True)
        self.horizontalLayout_2.addWidget(self.FromIDLine)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.ContentText = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.ContentText.setObjectName("ContentText")
        self.ContentText.setReadOnly(True)
        self.horizontalLayout_3.addWidget(self.ContentText)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.MessageExitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.MessageExitButton.setObjectName("MessageExitButton")
        self.MessageExitButton.setIcon(QtGui.QIcon('icon/confirm.ico'))
        self.MessageExitButton.clicked.connect(self.exit)
        self.horizontalLayout_4.addWidget(self.MessageExitButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MessageBox"))
        self.label.setText(_translate("Dialog", "You have got new message!"))
        self.label_2.setText(_translate("Dialog", "From:"))
        self.label_3.setText(_translate("Dialog", "Content:"))
        self.MessageExitButton.setText(_translate("Dialog", "OK"))

        file = QtCore.QFile('black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()
    
    def exit(self):
        self.FromIDLine.clear()
        self.ContentText.clear()
        self.hide()

    def setup(self,dic):
        self.FromIDLine.setText(dic["from_id"])
        self.ContentText.setText(dic["content"])

        ag = QApplication.desktop().availableGeometry()
        sg = QApplication.desktop().screenGeometry()
        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y) #使位置稍稍倾斜，防止消息弹窗被挡住

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = MessageBox_Dialog()
    
    dic={}
    dic["from_id"]=""
    dic["content"]=""
    window.setup(dic)



    sys.exit(app.exec_()) 