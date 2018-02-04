# -*- coding: utf-8 -*-

#Designed by Ao Wang, 15300240004

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog,  QListWidgetItem
import os
import sys
from socket import *
import json
sys.path.append("IP.py")
import IP as ip

class Admin_CustomerList_Dialog(QDialog): #当前店内用户窗口
    def __init__(self,parent=None):
        super(Admin_CustomerList_Dialog,self).__init__(parent)
        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(300, 380)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 260, 340))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CustomerList = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.CustomerList.setObjectName("CustomerList")
        self.verticalLayout.addWidget(self.CustomerList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.ExitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ExitButton.setObjectName("ExitButton")
        self.ExitButton.setIcon(QtGui.QIcon('icon/redcross.ico'))
        self.ExitButton.clicked.connect(self.exit)
        self.horizontalLayout.addWidget(self.ExitButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Customer List"))
        self.ExitButton.setText(_translate("Dialog", "Exit"))

        file = QtCore.QFile('black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()
    
    def exit(self):
        self.CustomerList.clear()
        self.hide()
    
    def closeEvent(self, event):#处理点击红叉的情况
        self.CustomerList.clear()
        event.accept()
    
    def reveice_data(self,dic):
        i=0
        for key in dic:
            string="   "+str(dic[key])
            item=QListWidgetItem()
            item.setIcon(QtGui.QIcon('icon/list.ico'))
            item.setText(string)
            self.CustomerList.insertItem(i,item)
            i+=1
        self.show()

class Admin_GoodsList_Dialog(QDialog):    #商店商品窗口
    cus_list = QtCore.pyqtSignal(dict)
    exit_shop = QtCore.pyqtSignal(dict)
    act_fail = QtCore.pyqtSignal()
    remain_update = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(Admin_GoodsList_Dialog,self).__init__(parent)
        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(500, 380)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 30, 150, 320))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.UserNameLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.UserNameLine.setObjectName("UserNameLine")
        self.UserNameLine.setReadOnly(True)
        self.verticalLayout.addWidget(self.UserNameLine)
        self.CurrentShopIDLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.CurrentShopIDLine.setObjectName("CurrentShopIDLine")
        self.CurrentShopIDLine.setReadOnly(True)
        self.verticalLayout.addWidget(self.CurrentShopIDLine)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.ExitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ExitButton.setObjectName("ExitButton")
        self.ExitButton.setIcon(QtGui.QIcon('icon/redcross.ico'))
        self.ExitButton.clicked.connect(self.exit)
        self.horizontalLayout_2.addWidget(self.ExitButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.ShowCustomerButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ShowCustomerButton.setObjectName("ShowCustomerButton")
        self.ShowCustomerButton.clicked.connect(self.get_customer_in_shop)
        self.ShowCustomerButton.setIcon(QtGui.QIcon('icon/list.ico'))
        self.horizontalLayout_3.addWidget(self.ShowCustomerButton)
        spacerItem4 = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(210, 30, 260, 320))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.Goods_SearchButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.Goods_SearchButton.setObjectName("Goods_SearchButton")
        self.Goods_SearchButton.clicked.connect(self.search_goods)
        self.Goods_SearchButton.setIcon(QtGui.QIcon('icon/query.ico'))
        self.horizontalLayout.addWidget(self.Goods_SearchButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.GoodsClearButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.GoodsClearButton.setObjectName("GoodsClearButton")
        self.GoodsClearButton.clicked.connect(self.good_clear)
        self.GoodsClearButton.setIcon(QtGui.QIcon('icon/empty.ico'))
        self.horizontalLayout.addWidget(self.GoodsClearButton)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Goods"))
        self.ExitButton.setText(_translate("Dialog", "Exit"))
        self.ShowCustomerButton.setText(_translate("Dialog", "Customer"))
        self.Goods_SearchButton.setText(_translate("Dialog", "Search"))
        self.GoodsClearButton.setText(_translate("Dialog", "Clear"))

        file = QtCore.QFile('black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()
    
    def receive_info(self,dic): #获取当前顾客信息
        self.show()
        self.shop_id=dic["shop_id"]
        self.user_id=dic["admin_id"]
        self.UserNameLine.setText("Current Admin: "+dic["admin_name"])
        self.CurrentShopIDLine.setText("Current Shop: "+str(dic["shop_id"]))

    def exit(self):
        self.CurrentShopIDLine.clear()
        self.listWidget.clear()
        self.UserNameLine.clear()
        self.hide()
    
    def search_goods(self): #获取当前商店的商品信息
        self.listWidget.clear()
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="getgoods"
        info["shop_id"]=str(self.shop_id)
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)

        goods_dic=eval(data)
        self.goods_id={}
        self.goods_name={}
        self.goods_price={}
        goods_num=len(goods_dic)
        for i in range(goods_num):
            if str(goods_dic[str(i)]["num"])!='0':
                string="Good Name: "+goods_dic[str(i)]["good_name"]+"\n"+"Good ID: "+goods_dic[str(i)]["good_id"]+"\n"+"Good Price: "+goods_dic[str(i)]["price"]+"\n"+"Num Left: "+str(goods_dic[str(i)]["num"])
                item=QListWidgetItem()
                item.setIcon(QtGui.QIcon('icon/list.ico'))
                item.setText(string)
                self.goods_id[i]=(int(goods_dic[str(i)]["good_id"]))
                self.goods_name[i]=goods_dic[str(i)]["good_name"]
                ss=goods_dic[str(i)]["price"]
                ss=ss.replace("$","")
                self.goods_price[i]=float(ss)
                self.listWidget.insertItem(i,item)
        s.close()
    
    def good_clear(self):
        self.listWidget.clear()
    
    def get_customer_in_shop(self): #获取当前店内顾客信息
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="get_customer_in_shop"
        info["shop_id"]=str(self.shop_id)
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        data=eval(data)

        self.cus_list.emit(data)   
    
if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = Admin_CustomerList_Dialog()
    window.show()
    sys.exit(app.exec_()) 