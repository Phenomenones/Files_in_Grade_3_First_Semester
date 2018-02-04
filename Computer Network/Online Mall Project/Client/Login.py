# -*- coding: utf-8 -*-

#Designed by Ao Wang, 15300240004

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
import os
import sys
from socket import *
import json
sys.path.append("IP.py")
import IP as ip

class Login_Dialog(QDialog):
    login_fail = QtCore.pyqtSignal()
    login_succeed_user = QtCore.pyqtSignal(dict)
    login_succeed_admin = QtCore.pyqtSignal(dict)

    def __init__(self,parent=None):
        super(Login_Dialog,self).__init__(parent)

        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(410, 230)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 350, 170))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.TopLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.TopLabel.setObjectName("TopLabel")
        self.horizontalLayout.addWidget(self.TopLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.PasswordLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.PasswordLabel.setObjectName("PasswordLabel")
        self.gridLayout.addWidget(self.PasswordLabel, 1, 0, 1, 1)
        self.IDLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.IDLabel.setObjectName("IDLabel")
        self.gridLayout.addWidget(self.IDLabel, 0, 0, 1, 1)
        self.IDLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.IDLine.setObjectName("IDLine")
        self.gridLayout.addWidget(self.IDLine, 0, 1, 1, 1)
        self.PasswordLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.PasswordLine.setObjectName("PasswordLine")
        self.PasswordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.PasswordLine, 1, 1, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.LoginButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.LoginButton.setObjectName("LoginButton")
        self.LoginButton.setIcon(QtGui.QIcon('icon/confirm.ico'))
        self.LoginButton.clicked.connect(self.send_message)
        self.horizontalLayout_2.addWidget(self.LoginButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.ClearButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ClearButton.setObjectName("ClearButton")
        self.ClearButton.setIcon(QtGui.QIcon('icon/empty.ico'))
        self.ClearButton.clicked.connect(self.clear)
        self.horizontalLayout_2.addWidget(self.ClearButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "User Login"))
        self.TopLabel.setText(_translate("Dialog", "Simple&Naive Online Mall"))
        self.PasswordLabel.setText(_translate("Dialog", "Password:"))
        self.IDLabel.setText(_translate("Dialog", "User ID："))
        self.LoginButton.setText(_translate("Dialog", "Login"))
        self.ClearButton.setText(_translate("Dialog", "Clear"))

        file = QtCore.QFile('black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()
    
    def clear(self):
        self.IDLine.setText("")
        self.PasswordLine.setText("")
    
    def show_myself(self):
        self.clear()
        self.show()
    
    def send_message(self): #发送登录信息
        ID=self.IDLine.text()
        PassWord=self.PasswordLine.text()
        addr=(ip.HOST,ip.PORT)
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="login"
        info["id"]=ID
        info["password"]=PassWord
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        self.PasswordLine.setText("")
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)

        res=eval(data)  #接收服务器发来的信息，传递相应信息
        if res["state"]=="fail":
            self.login_fail.emit()
        if res["state"]=="succeed":
            self.clear()
            self.hide()
            emit_dic={}
            emit_dic["id"]=res["id"]
            emit_dic["name"]=res["name"]
            if res["authority"] == "user":
                self.login_succeed_user.emit(emit_dic)
            elif res["authority"] == "admin":
                self.login_succeed_admin.emit(emit_dic)
            
        s.close()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = Login_Dialog()
    window.show()
    sys.exit(app.exec_()) 