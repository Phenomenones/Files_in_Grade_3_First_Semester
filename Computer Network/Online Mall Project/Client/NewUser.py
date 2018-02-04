# -*- coding: utf-8 -*-

#Designed by Ao Wang, 15300240004

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QAction, QListWidgetItem, QLabel
import sys
import os
from socket import *
import json
sys.path.append("IP.py")
import IP as ip

class Image(QLabel):   # 重载QLabel，方便拖拽式上传头像
    image_chose = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(Image, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()   # must accept the dragEnterEvent or else the dropEvent can't occur !!!
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():   # if file or link is dropped
            urlcount = len(event.mimeData().urls())  # count number of drops
            url = event.mimeData().urls()[0]   # get first url
            self.url = url.toString()
            self.image_chose.emit(self.url)
            #event.accept()  # doesnt appear to be needed

class NewUser_Dialog(QDialog):
    act_fail = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(NewUser_Dialog,self).__init__(parent)
        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(670, 390)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(360, 100, 270, 190))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.UserNameLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.UserNameLine.setObjectName("UserNameLine")
        self.horizontalLayout_4.addWidget(self.UserNameLine)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.UserPasswordLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.UserPasswordLine.setObjectName("UserPasswordLine")
        self.horizontalLayout_2.addWidget(self.UserPasswordLine)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.OKButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.OKButton.setObjectName("OKButton")
        self.OKButton.setIcon(QtGui.QIcon('icon/confirm.ico'))
        self.OKButton.clicked.connect(self.create_new_user)
        self.horizontalLayout.addWidget(self.OKButton)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.ClearButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ClearButton.setObjectName("ClearButton")
        self.ClearButton.setIcon(QtGui.QIcon('icon/empty.ico'))
        self.ClearButton.clicked.connect(self.clear_all)
        self.horizontalLayout.addWidget(self.ClearButton)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 60, 230, 300))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem9)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem10)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.HeadImage = Image(self.verticalLayoutWidget_2)
        self.HeadImage.setMinimumSize(QtCore.QSize(73, 0))
        self.HeadImage.setObjectName("HeadImage")
        self.HeadImage.setFixedSize(120,120)
        self.horizontalLayout_7.addWidget(self.HeadImage)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem11)
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(190, 20, 270, 20))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem12)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_8)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_8.addWidget(self.label_4)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem13)
        self.horizontalLayoutWidget_9 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_9.setGeometry(QtCore.QRect(310, 60, 20, 300))
        self.horizontalLayoutWidget_9.setObjectName("horizontalLayoutWidget_9")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget_9)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_9.addWidget(self.line)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.url="tmp/default.jpg"  #用于上传头像
        pixmap=QtGui.QPixmap(self.url).scaled(120, 120, transformMode=QtCore.Qt.SmoothTransformation)
        self.HeadImage.setPixmap(pixmap)

        #!!!!!!!!!!!!!!!!!!!!
        self.HeadImage.image_chose.connect(self.headimage_change)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New User Register"))
        self.label_2.setText(_translate("Dialog", "User Name:"))
        self.label_3.setText(_translate("Dialog", "User Password:"))
        self.OKButton.setText(_translate("Dialog", "OK"))
        self.ClearButton.setText(_translate("Dialog", "Clear"))
        self.label.setText(_translate("Dialog", "Drag and drop the head image here:"))
        self.HeadImage.setText(_translate("Dialog", "Head Image"))
        self.label_4.setText(_translate("Dialog", "New User Register"))

        file = QtCore.QFile('black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()
    
    def headimage_change(self,string):
        string=string[8:]   #去掉"file://""头部
        self.url=string
        pixmap=QtGui.QPixmap(self.url).scaled(120, 120, transformMode=QtCore.Qt.SmoothTransformation)
        self.HeadImage.setPixmap(pixmap)
    
    def show_win(self):
        self.show()
    
    def clear_all(self):
        self.UserNameLine.clear()
        self.UserPasswordLine.clear()
        self.url="tmp/default.jpg"
        pixmap=QtGui.QPixmap(self.url).scaled(120, 120, transformMode=QtCore.Qt.SmoothTransformation)
        self.HeadImage.setPixmap(pixmap)
    
    def closeEvent(self, event):#处理点击红叉的情况
        self.clear_all()
        event.accept()
    
    def create_new_user(self):
        '''
        Transfer name and password first,
        if the name is legal, then transfer the head image
        '''
        name=self.UserNameLine.text()
        password=self.UserPasswordLine.text()
        if "@" in name or "@" in password or(name == "" and password == ""):
            self.UserNameLine.clear()
            self.UserPasswordLine.clear()
            self.act_fail.emit()
            return
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="register_new_user"
        info["name"]=name
        info["password"]=password
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        data=eval(data)
        if data["state"]=="fail":
            self.UserNameLine.clear()
            self.UserPasswordLine.clear()
            self.act_fail.emit()
            return
        elif data["state"]=="succeed":
            path=self.url
            with open(path, 'rb') as f:
                data = f.read(ip.BUFFERSIZE)
                data=ip.encrypt(data)
                s.sendto(data,(ip.HOST,ip.HEADIMAGE_PORT))#用头像专用端口发送
            self.clear_all()
        s.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = NewUser_Dialog()
    window.show()
    sys.exit(app.exec_()) 

