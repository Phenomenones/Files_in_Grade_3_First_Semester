# -*- coding: utf-8 -*-

#Designed by Ao Wang, 15300240004

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QAction, QListWidgetItem
from PyQt5.QtCore import QThread, QObject, QTimer
import sys
import os
from socket import *
import json
sys.path.append("IP.py")
import IP as ip
import time

class get_newest_message(QObject):  #额外线程运行的对象
    new_message = QtCore.pyqtSignal(dict)
    def setup(self,dic):
        id_num=dic["id"]
        self.id_num=id_num
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.initial)
        self.timer.start(500)

        self.widget=dic["widget"]
    
    def initial(self):
        self.get_message(self.id_num)

    def get_message(self,user_id):  #不断联系服务器尝试获取最新消息
        try:
            self.rec_soc=socket(AF_INET,SOCK_DGRAM)
            timeout = ip.TIMEOUT
            self.rec_soc.settimeout(timeout)
            info={}
            info["request"]="get_newest_message"
            info["user_id"]=int(user_id)
            info["timestamp"]=ip.get_time_stamp()
            info = json.dumps(info)
            res=ip.encrypt(info)#encrypt
            self.rec_soc.sendto(res,(ip.HOST,ip.PORT))
            data,ADDR = self.rec_soc.recvfrom(ip.BUFFERSIZE)
            data=ip.decrypt(data)
            data=eval(data)
            self.rec_soc.close()
            if data["state"] == "fail":
                return
            elif data["state"] == "succeed":
                data["widget"]=self.widget
                self.new_message.emit(data)
                return
        except:
            return
    
    def close_socket(self):
        self.rec_soc.close()


class Userinterface_Dialog(QDialog):    #用户界面
    this_hide = QtCore.pyqtSignal()
    shop_chose = QtCore.pyqtSignal(dict)
    myshop = QtCore.pyqtSignal(dict)
    act_fail = QtCore.pyqtSignal()
    new_message = QtCore.pyqtSignal(dict)
    test_signal = QtCore.pyqtSignal(dict)
    close_socket = QtCore.pyqtSignal()

    def __init__(self,parent=None):
        super(Userinterface_Dialog,self).__init__(parent)
        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(720, 520)
        self.TopLabel = QtWidgets.QLabel(Dialog)
        self.TopLabel.setGeometry(QtCore.QRect(250, 10, 220, 20))
        self.TopLabel.setObjectName("TopLabel")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(180, 60, 510, 410))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(70, 20, 370, 340))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ShopList = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.ShopList.setObjectName("ShopList")
        self.verticalLayout.addWidget(self.ShopList)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Shop_SearchButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.Shop_SearchButton.setObjectName("Shop_SearchButton")
        self.Shop_SearchButton.setIcon(QtGui.QIcon('icon/query.ico'))
        self.Shop_SearchButton.clicked.connect(self.get_shop_info)
        self.horizontalLayout.addWidget(self.Shop_SearchButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.Shop_ClearButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.Shop_ClearButton.setObjectName("Shop_ClearButton")
        self.Shop_ClearButton.setIcon(QtGui.QIcon('icon/empty.ico'))
        self.Shop_ClearButton.clicked.connect(self.shop_clear)
        self.horizontalLayout.addWidget(self.Shop_ClearButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(70, 20, 370, 340))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.Date1 = QtWidgets.QDateEdit(self.verticalLayoutWidget_4)
        self.Date1.setObjectName("Date1")
        self.Date1.setDisplayFormat("yyyy-MM-dd")
        self.Date1.setDateTime(QtCore.QDateTime(QtCore.QDate(2017, 1, 1)))
        self.horizontalLayout_2.addWidget(self.Date1)
        self.ToLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.ToLabel.setObjectName("ToLabel")
        self.horizontalLayout_2.addWidget(self.ToLabel, 0, QtCore.Qt.AlignHCenter)
        self.Date2 = QtWidgets.QDateEdit(self.verticalLayoutWidget_4)
        self.Date2.setObjectName("Date2")
        self.Date2.setDisplayFormat("yyyy-MM-dd")
        self.Date2.setDateTime(QtCore.QDateTime(QtCore.QDate(2017, 12, 31)))
        self.horizontalLayout_2.addWidget(self.Date2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.InfoList = QtWidgets.QListWidget(self.verticalLayoutWidget_4)
        self.InfoList.setObjectName("InfoList")
        self.verticalLayout_3.addWidget(self.InfoList)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.Info_SearchButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Info_SearchButton.setObjectName("Info_SearchButton")
        self.Info_SearchButton.setIcon(QtGui.QIcon('icon/query.ico'))
        self.Info_SearchButton.clicked.connect(self.get_message)
        self.horizontalLayout_3.addWidget(self.Info_SearchButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.Info_ClearButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Info_ClearButton.setObjectName("Info_ClearButton")
        self.Info_ClearButton.setIcon(QtGui.QIcon('icon/empty.ico'))
        self.Info_ClearButton.clicked.connect(self.info_clear)
        self.horizontalLayout_3.addWidget(self.Info_ClearButton)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 60, 140, 410))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.CurrentUserName = QtWidgets.QLineEdit(self.verticalLayoutWidget_5)
        self.CurrentUserName.setObjectName("CurrentUserName")
        self.CurrentUserName.setReadOnly(True)
        self.horizontalLayout_7.addWidget(self.CurrentUserName)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.HeadImage = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.HeadImage.setObjectName("HeadImage")
        self.HeadImage.setFixedHeight(120)
        self.HeadImage.setFixedWidth(120)
        self.horizontalLayout_6.addWidget(self.HeadImage)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem8)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem9 = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.MyShopButton = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.MyShopButton.setObjectName("MyShopButton")
        self.MyShopButton.clicked.connect(self.MyShop_chose)
        self.MyShopButton.setIcon(QtGui.QIcon('icon/get.ico'))
        self.horizontalLayout_4.addWidget(self.MyShopButton)
        spacerItem10 = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem10)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem11)
        self.ExitButton = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.ExitButton.setObjectName("ExitButton")
        self.ExitButton.setIcon(QtGui.QIcon('icon/redcross.ico'))
        self.ExitButton.clicked.connect(self.exit)
        self.horizontalLayout_5.addWidget(self.ExitButton)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem12)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayoutWidget11 = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget11.setGeometry(QtCore.QRect(80, 100, 370, 180))
        self.verticalLayoutWidget11.setObjectName("verticalLayoutWidget11")
        self.verticalLayout_211 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget11)
        self.verticalLayout_211.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_211.setObjectName("verticalLayout_211")
        self.horizontalLayout_211 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_211.setObjectName("horizontalLayout_211")
        self.label11 = QtWidgets.QLabel(self.verticalLayoutWidget11)
        self.label11.setObjectName("label11")
        self.horizontalLayout_211.addWidget(self.label11)
        self.RemainingNumLine = QtWidgets.QLineEdit(self.verticalLayoutWidget11)
        self.RemainingNumLine.setObjectName("RemainingNumLine")
        self.RemainingNumLine.setReadOnly(True)
        self.horizontalLayout_211.addWidget(self.RemainingNumLine)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_211.addItem(spacerItem)
        self.verticalLayout_211.addLayout(self.horizontalLayout_211)
        self.horizontalLayout_411 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_411.setObjectName("horizontalLayout_411")
        self.label_211 = QtWidgets.QLabel(self.verticalLayoutWidget11)
        self.label_211.setObjectName("label_211")
        self.horizontalLayout_411.addWidget(self.label_211)
        self.verticalLayout_211.addLayout(self.horizontalLayout_411)
        self.horizontalLayout_311 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_311.setObjectName("horizontalLayout_311")
        spacerItem111 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_311.addItem(spacerItem111)
        self.label_311 = QtWidgets.QLabel(self.verticalLayoutWidget11)
        self.label_311.setObjectName("label_311")
        self.horizontalLayout_311.addWidget(self.label_311)
        self.InputLine = QtWidgets.QLineEdit(self.verticalLayoutWidget11)
        self.InputLine.setObjectName("InputLine")
        self.horizontalLayout_311.addWidget(self.InputLine)
        spacerItem211 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_311.addItem(spacerItem211)
        self.verticalLayout_211.addLayout(self.horizontalLayout_311)
        self.horizontalLayout11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout11.setObjectName("horizontalLayout11")
        spacerItem311 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout11.addItem(spacerItem311)
        self.AccountEnsureButton = QtWidgets.QPushButton(self.verticalLayoutWidget11)
        self.AccountEnsureButton.setObjectName("AccountEnsureButton")
        self.AccountEnsureButton.setIcon(QtGui.QIcon('icon/confirm.ico'))
        self.AccountEnsureButton.clicked.connect(self.charge_money)
        self.horizontalLayout11.addWidget(self.AccountEnsureButton)
        spacerItem411 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout11.addItem(spacerItem411)
        self.AccountClearButton = QtWidgets.QPushButton(self.verticalLayoutWidget11)
        self.AccountClearButton.setObjectName("AccountClearButton")
        self.AccountClearButton.setIcon(QtGui.QIcon('icon/empty.ico'))
        self.AccountClearButton.clicked.connect(self.InputLine_clear)
        self.horizontalLayout11.addWidget(self.AccountClearButton)
        spacerItem511 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout11.addItem(spacerItem511)
        self.verticalLayout_211.addLayout(self.horizontalLayout11)
        self.tabWidget.addTab(self.tab_3, "My Account")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.ShopList.itemClicked.connect(self.item_clicked)#!!!!!!!!!!

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "User Interface"))
        self.TopLabel.setText(_translate("Dialog", "Simple&Naive Mall User Interface"))
        self.Shop_SearchButton.setText(_translate("Dialog", "Search"))
        self.Shop_ClearButton.setText(_translate("Dialog", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Shop Info"))
        self.ToLabel.setText(_translate("Dialog", "To"))
        self.Info_SearchButton.setText(_translate("Dialog", "Search"))
        self.Info_ClearButton.setText(_translate("Dialog", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Message"))
        self.MyShopButton.setText(_translate("Dialog", "MyShop"))
        self.ExitButton.setText(_translate("Dialog", "Exit"))
        self.label11.setText(_translate("Dialog", "Current Remaining:"))
        self.label_211.setText(_translate("Dialog", "Input the num of money you want to charge:"))
        self.label_311.setText(_translate("Dialog", "$"))
        self.AccountEnsureButton.setText(_translate("Dialog", "OK"))
        self.AccountClearButton.setText(_translate("Dialog", "Clear"))

        file = QtCore.QFile('black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()
    
    def get_remaining(self):    #获得余额,记得买东西时要用这个函数修改！！！！！！！！！！！！
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="get_user_remaining"
        info["user_id"] = self.id
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        data=eval(data)
        string="$"+str(data["remaining"])
        self.RemainingNumLine.setText(string)

    def receive_user_argument(self,dic):    #接收用户信息
        self.show()
        self.id=dic["id"]
        self.name=dic["name"]
        self.CurrentUserName.setText(str("User: " + self.name))
        self.HeadImage.clear()
        self.InputLine.clear()
        self.RemainingNumLine.clear()

        self.get_remaining() #获得余额

        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="headimage"
        info["id"]=self.id
        info["authority"]="user"
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)

        with open('tmp/image.jpg', 'ab') as f:  #显示接收的用户头像
            f.write(data)
        
        pixmap=QtGui.QPixmap("tmp/image.jpg").scaled(120, 120, transformMode=QtCore.Qt.SmoothTransformation)
        self.HeadImage.setPixmap(pixmap)

        os.remove(str("tmp/image.jpg"))#attention
        s.close()

        self.newthread()    #开启新的进程，尝试从服务器获取最新消息

    def newthread(self):
        self.listenthread=QThread()
        self.get_message=get_newest_message()

        self.get_message.moveToThread(self.listenthread)    #开始新线程

        self.messagebox_win = ip.MessageBox_Dialog()#newly added
        self.get_message.new_message.connect(self.messagebox_win.setup)

        #QtCore.Qt.QueuedConnection
        self.listenthread.started.connect(self.transmit)
        self.test_signal.connect(self.get_message.setup)
        self.close_socket.connect(self.closethread)
        self.listenthread.start()

    def closethread(self):
        self.get_message.close_socket()
        self.listenthread.quit()

    def transmit(self):
        dic={}
        dic["id"]=int(self.id)
        dic["widget"]=self.ExitButton
        self.test_signal.emit(dic)
    
    def closeEvent(self, event):    #处理点击红叉的情况
        self.close_socket.emit()
        event.accept()

    def exit(self): #退出用户界面
        self.hide()
        self.this_hide.emit()
        self.close_socket.emit()
        self.ShopList.clear()
        self.InfoList.clear()
    
    def get_shop_info(self):    #接收商店信息
        self.ShopList.clear()
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="shopinfo"
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        shop_dic=eval(data)

        self.shop_id=[]
        shop_num=len(shop_dic)
        for i in range(shop_num):
            string="Shop Name: "+shop_dic[str(i)]["shopname"]+"\n"+"Owner ID: "+shop_dic[str(i)]["id"]+"\n"+"Owner name: "+shop_dic[str(i)]["ownername"]+'\n'
            item=QListWidgetItem()
            item.setIcon(QtGui.QIcon('icon/shop.ico'))
            item.setText(string)
            self.shop_id.append(int(shop_dic[str(i)]["id"]))
            self.ShopList.insertItem(i,item)
        s.close()

    def item_clicked(self,item):    #用户点击商店后，发送信息
        dic={}
        dic["shop_id"]=self.shop_id[self.ShopList.currentRow()]
        dic["user_id"]=self.id
        dic["user_name"]=self.name
        self.shop_chose.emit(dic)
        self.hide
    
    def shop_clear(self):
        self.ShopList.clear()
    
    def get_message(self):  #根据时间区间获得消息信息
        self.InfoList.clear()
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="messageinfo"
        info["date1"] = self.Date1.text()
        info["date2"] = self.Date2.text()
        info["id"] = self.id
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        message_dic=eval(data)

        message_num=len(message_dic)
        for i in range(message_num):    #拼装信息
            string="Date: "+message_dic[str(i)]["date"]+"\n"+"Time: "+message_dic[str(i)]["time"]+"\n"+"From: "+message_dic[str(i)]["from"]+"\n"+"Content: "+message_dic[str(i)]["content"]+'\n'
            item=QListWidgetItem()
            item.setIcon(QtGui.QIcon('icon/list.ico'))
            item.setText(string)
            self.InfoList.insertItem(i,item)
        self.InfoList.sortItems()
        s.close()
    
    def info_clear(self):
        self.InfoList.clear()
    
    def user_leave_shop(self,dic):  #发送用户离开商店信号
        self.InfoList.clear()
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="user_leave_shop"
        info["user_id"] = dic["user_id"]
        info["owner_id"] = dic["owner_id"]
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        s.close()
    
    def MyShop_chose(self): #用户点击进入自己的商店
        tmp={}
        tmp["ownername"]=self.name
        tmp["shopid"]=self.id
        self.myshop.emit(tmp)
    
    def InputLine_clear(self):
        self.InputLine.clear()
    
    def charge_money(self):
        #act_fail = QtCore.pyqtSignal()
        num=self.InputLine.text()
        num_ = num.replace('.', '')
        if not (num.isdigit() or num_.isdigit()):#not safe!!!!!!!!
            self.act_fail.emit()
            self.InputLine.clear()
            return
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="charge_money"
        info["user_id"] = str(self.id)
        info["num"] = num
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        data=eval(data)

        string="$"+str(data["remaining"])
        self.RemainingNumLine.setText(string)
        s.close()
        self.InputLine.clear()
    



if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = Userinterface_Dialog()
    window.show()
    sys.exit(app.exec_()) 