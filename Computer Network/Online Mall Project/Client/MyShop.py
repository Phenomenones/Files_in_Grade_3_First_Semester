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

class MyShop_Dialog(QDialog):   #我的商店信息
    act_fail = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(MyShop_Dialog,self).__init__(parent)
        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(650, 435)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(170, 40, 430, 350))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 70, 330, 160))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.GoodPriceLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.GoodPriceLabel.setObjectName("GoodPriceLabel")
        self.gridLayout.addWidget(self.GoodPriceLabel, 1, 0, 1, 1)
        self.GoodPriceLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.GoodPriceLine.setObjectName("GoodPriceLine")
        self.gridLayout.addWidget(self.GoodPriceLine, 1, 1, 1, 1)
        self.GoodNameLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.GoodNameLine.setObjectName("GoodNameLine")
        self.gridLayout.addWidget(self.GoodNameLine, 0, 1, 1, 1)
        self.GoodNameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.GoodNameLabel.setObjectName("GoodNameLabel")
        self.gridLayout.addWidget(self.GoodNameLabel, 0, 0, 1, 1)
        self.GoodNumLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.GoodNumLabel.setObjectName("GoodNumLabel")
        self.gridLayout.addWidget(self.GoodNumLabel, 2, 0, 1, 1)
        self.GoodNumLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.GoodNumLine.setObjectName("GoodNumLine")
        self.gridLayout.addWidget(self.GoodNumLine, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.GoodEnsureButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.GoodEnsureButton.setObjectName("GoodEnsureButton")
        self.GoodEnsureButton.setIcon(QtGui.QIcon('icon/confirm.ico'))
        self.GoodEnsureButton.clicked.connect(self.register_new_good)
        self.horizontalLayout.addWidget(self.GoodEnsureButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.GoodClearButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.GoodClearButton.setObjectName("GoodClearButton")
        self.GoodClearButton.setIcon(QtGui.QIcon('icon/empty.ico'))
        self.GoodClearButton.clicked.connect(self.new_good_clear)
        self.horizontalLayout.addWidget(self.GoodClearButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(50, 30, 330, 250))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.CustomerList = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.CustomerList.setObjectName("CustomerList")
        self.verticalLayout_2.addWidget(self.CustomerList)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.GetCustomerButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.GetCustomerButton.setObjectName("GetCustomerButton")
        self.GetCustomerButton.setIcon(QtGui.QIcon('icon/get.ico'))
        self.GetCustomerButton.clicked.connect(self.get_customer_in_shop)
        self.horizontalLayout_2.addWidget(self.GetCustomerButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.CustomerClearbutton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.CustomerClearbutton.setObjectName("CustomerClearbutton")
        self.CustomerClearbutton.setIcon(QtGui.QIcon('icon/empty.ico'))
        self.CustomerClearbutton.clicked.connect(self.customer_clear)
        self.horizontalLayout_2.addWidget(self.CustomerClearbutton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(50, 30, 330, 250))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.GoodList = QtWidgets.QListWidget(self.verticalLayoutWidget_3)
        self.GoodList.setObjectName("GoodList")
        self.verticalLayout_3.addWidget(self.GoodList)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.GetGoodButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.GetGoodButton.setObjectName("GetGoodButton")
        self.GetGoodButton.setIcon(QtGui.QIcon('icon/get.ico'))
        self.GetGoodButton.clicked.connect(self.get_goods_in_myshop)
        self.horizontalLayout_3.addWidget(self.GetGoodButton)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.GoodClearbutton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.GoodClearbutton.setObjectName("GoodClearbutton")
        self.GoodClearbutton.setIcon(QtGui.QIcon('icon/empty.ico'))
        self.GoodClearbutton.clicked.connect(self.good_clear)
        self.horizontalLayout_3.addWidget(self.GoodClearbutton)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(30, 50, 110, 340))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.OwnerNameLine = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.OwnerNameLine.setObjectName("OwnerNameLine")
        self.OwnerNameLine.setReadOnly(True)
        self.verticalLayout_4.addWidget(self.OwnerNameLine)
        self.ShopIDLine = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.ShopIDLine.setObjectName("ShopIDLine")
        self.ShopIDLine.setReadOnly(True)
        self.verticalLayout_4.addWidget(self.ShopIDLine)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem10)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem11)
        self.QuitButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.QuitButton.setObjectName("QuitButton")
        self.QuitButton.setIcon(QtGui.QIcon('icon/redcross.ico'))
        self.QuitButton.clicked.connect(self.exit)
        self.horizontalLayout_4.addWidget(self.QuitButton)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem12)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "My Shop"))
        self.GoodPriceLabel.setText(_translate("Dialog", "Product Price:"))
        self.GoodNameLabel.setText(_translate("Dialog", "Product Name:"))
        self.GoodNumLabel.setText(_translate("Dialog", "Number:"))
        self.GoodEnsureButton.setText(_translate("Dialog", "OK"))
        self.GoodClearButton.setText(_translate("Dialog", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "New Product"))
        self.GetCustomerButton.setText(_translate("Dialog", "Get"))
        self.CustomerClearbutton.setText(_translate("Dialog", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Customer Now"))
        self.GetGoodButton.setText(_translate("Dialog", "Get"))
        self.GoodClearbutton.setText(_translate("Dialog", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Products"))
        self.QuitButton.setText(_translate("Dialog", "Quit"))

        file = QtCore.QFile('black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()
    
    def get_owner(self,dic):    #获得基本信息
        self.OwnerNameLine.setText("Owner: "+str(dic["ownername"]))
        self.id=int(dic["shopid"])
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="if_shop_exists"
        info["user_id"]=str(self.id)
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        data=eval(data)

        if data["shop_name"]!="none":
            self.ShopIDLine.setText("Shop Name: "+ data["shop_name"])
            self.shopid=str(dic["shopid"])
            self.show()
        else: 
            self.act_fail.emit()
    
    def exit(self):
        self.OwnerNameLine.clear()
        self.ShopIDLine.clear()
        self.GoodNameLine.clear()
        self.GoodPriceLine.clear()
        self.GoodNumLine.clear()
        self.CustomerList.clear()
        self.GoodList.clear()
        self.hide()
    
    def new_good_clear(self):
        self.GoodNameLine.clear()
        self.GoodPriceLine.clear()
        self.GoodNumLine.clear()
    
    def customer_clear(self):
        self.CustomerList.clear()
    
    def good_clear(self):
        self.GoodList.clear()

    def register_new_good(self):    #登记新商品
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="register_new_good"
        info["goodname"] = self.GoodNameLine.text()
        info["goodprice"] = self.GoodPriceLine.text()
        info["goodnum"] = self.GoodNumLine.text()
        info["shopid"] = self.shopid
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        data=eval(data)
        if data["state"]=="fail":
            self.act_fail.emit()
        s.close()
        #broadcast to the customers in the shop
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="get_customer_in_shop"
        info["shop_id"]=str(self.shopid)
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        data=eval(data)
        info={}
        info["request"] = "inform_new_good"
        info["shop_id"] = str(self.shopid)
        info["goodname"] = self.GoodNameLine.text()
        info["customer"] = data
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        self.new_good_clear()
        s.close()
    
    def get_customer_in_shop(self): #获取当前店内顾客
        self.CustomerList.clear()
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="get_customer_in_shop"
        info["shop_id"]=str(self.shopid)
        info["timestamp"]=ip.get_time_stamp()
        info = json.dumps(info)
        res=ip.encrypt(info)#encrypt
        s.sendto(res,(ip.HOST,ip.PORT))
        data,ADDR = s.recvfrom(ip.BUFFERSIZE)
        data=ip.decrypt(data)
        dic=eval(data)
        i=0
        for key in dic:
            string="   "+str(dic[key])
            item=QListWidgetItem()
            item.setIcon(QtGui.QIcon('icon/list.ico'))
            item.setText(string)
            self.CustomerList.insertItem(i,item)
            i+=1
        s.close()
    
    def get_goods_in_myshop(self):  #获取店内商品
        self.GoodList.clear()
        s=socket(AF_INET,SOCK_DGRAM)
        timeout = ip.TIMEOUT
        s.settimeout(timeout)
        info={}
        info["request"]="getgoods"
        info["shop_id"]=str(self.shopid)
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
                self.goods_price[i]=goods_dic[str(i)]["price"]
                self.GoodList.insertItem(i,item)
        s.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = MyShop_Dialog()
    window.show()
    sys.exit(app.exec_()) 