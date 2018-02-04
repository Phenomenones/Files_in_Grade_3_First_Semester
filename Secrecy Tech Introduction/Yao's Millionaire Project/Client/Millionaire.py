# -*- coding: utf-8 -*-
#Designed by Ao Wang, 15300240004

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QByteArray, QTextStream
import os
import sys
from socket import *
import json
sys.path.append("Client.py")
import Client as client

class Error_Dialog(QDialog):
    def __init__(self,parent=None):
        super(Error_Dialog,self).__init__(parent)
        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 130)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 20, 250, 40))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(50, 70, 250, 40))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setIcon(QtGui.QIcon('decorate/redcross.ico'))
        self.pushButton.clicked.connect(self.quit)
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "错误！"))
        self.label.setText(_translate("Dialog", "您的操作出现错误，请重新尝试！"))
        self.pushButton.setText(_translate("Dialog", "退出"))
        file = QtCore.QFile('decorate/black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet=QTextStream(styleSheet).readAll()
        self.setStyleSheet(styleSheet)
        file.close()
    
    def quit(self):
        self.hide()

class Millionaire_Dialog(QDialog):
    action_fail = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(Millionaire_Dialog,self).__init__(parent)

        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(670, 680)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(120, 330, 60, 15))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(80, 30, 510, 20))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 90, 510, 130))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.MoneyLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.MoneyLine.setObjectName("MoneyLine")
        self.gridLayout.addWidget(self.MoneyLine, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.WantNameLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.WantNameLine.setObjectName("WantNameLine")
        self.gridLayout.addWidget(self.WantNameLine, 2, 1, 1, 1)
        self.MyNameLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.MyNameLine.setObjectName("MyNameLine")
        self.gridLayout.addWidget(self.MyNameLine, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.Show_Hide_Button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Show_Hide_Button.setObjectName("Show_Hide_Button")
        self.Show_Hide_Button.setIcon(QtGui.QIcon('decorate/eye.ico'))
        self.Show_Hide_Button.clicked.connect(self.hide_show)
        self.gridLayout.addWidget(self.Show_Hide_Button, 1, 2, 1, 1)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(80, 220, 510, 30))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.Ensurebutton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.Ensurebutton.setObjectName("Ensurebutton")
        self.Ensurebutton.setIcon(QtGui.QIcon('decorate/confirm.ico'))
        self.Ensurebutton.clicked.connect(self.process)
        self.horizontalLayout_3.addWidget(self.Ensurebutton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.PartClearButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.PartClearButton.setObjectName("PartClearButton")
        self.PartClearButton.setIcon(QtGui.QIcon('decorate/empty.ico'))
        self.PartClearButton.clicked.connect(self.part_clear)
        self.horizontalLayout_3.addWidget(self.PartClearButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 270, 570, 40))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(80, 330, 510, 130))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.Ten_Interger_Line = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.Ten_Interger_Line.setObjectName("Ten_Interger_Line")
        self.gridLayout_2.addWidget(self.Ten_Interger_Line, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.BigIntergerLine = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.BigIntergerLine.setObjectName("BigIntergerLine")
        self.horizontalLayout_4.addWidget(self.BigIntergerLine)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem9)
        self.The_j_th_num_Line = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.The_j_th_num_Line.setObjectName("The_j_th_num_Line")
        self.horizontalLayout_5.addWidget(self.The_j_th_num_Line)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 2, 1, 1, 1)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(50, 480, 570, 40))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem11)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem12)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(80, 540, 510, 100))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem13)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem14)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem15 = QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem15)
        self.ResultLine = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.ResultLine.setObjectName("ResultLine")
        self.horizontalLayout_7.addWidget(self.ResultLine)
        spacerItem16 = QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem16)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem17)
        self.AllClearButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.AllClearButton.setObjectName("AllClearButton")
        self.AllClearButton.setIcon(QtGui.QIcon('decorate/empty.ico'))
        self.AllClearButton.clicked.connect(self.all_clear)
        self.horizontalLayout_8.addWidget(self.AllClearButton)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem18)
        self.ExitButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.ExitButton.setObjectName("ExitButton")
        self.ExitButton.setIcon(QtGui.QIcon('decorate/redcross.ico'))
        self.ExitButton.clicked.connect(self.exit)
        self.horizontalLayout_8.addWidget(self.ExitButton)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem19)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "百万富翁问题 测试系统"))
        self.label.setText(_translate("Dialog", "百万富翁问题 测试系统"))
        self.label_2.setText(_translate("Dialog", "请输入您的姓名："))
        self.label_8.setText(_translate("Dialog", "请输入您要对比的人的姓名："))
        self.label_3.setText(_translate("Dialog", "请输入您的财产(1至10之间)："))
        self.Show_Hide_Button.setText(_translate("Dialog", "显示/隐藏"))
        self.Ensurebutton.setText(_translate("Dialog", "确认"))
        self.PartClearButton.setText(_translate("Dialog", "清空"))
        self.label_4.setText(_translate("Dialog", "您选择的随机大整数是："))
        self.label_6.setText(_translate("Dialog", "您收到的10个整数为："))
        self.label_7.setText(_translate("Dialog", "其中，第j个数为："))
        self.label_9.setText(_translate("Dialog", "最终结果是："))
        self.AllClearButton.setText(_translate("Dialog", "清空"))
        self.ExitButton.setText(_translate("Dialog", "退出"))

        file = QtCore.QFile('decorate/black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet=QTextStream(styleSheet).readAll()
        self.setStyleSheet(styleSheet)
        file.close()

        self.BigIntergerLine.setReadOnly(True)
        self.Ten_Interger_Line.setReadOnly(True)
        self.The_j_th_num_Line.setReadOnly(True)
        self.ResultLine.setReadOnly(True)

        self.error_win=Error_Dialog()

        self.action_fail.connect(self.error_deal)
        self.setWindowOpacity(0.97) #半透明
    
    def error_deal(self):   #发生错误，打开提示窗口
        self.all_clear()
        self.error_win.show()
    
    def exit(self): #退出
        self.close()
    
    def part_clear(self):   #清空输入部分
        self.MyNameLine.clear()
        self.MoneyLine.clear()
        self.WantNameLine.clear()
    
    def hide_show(self):    #转换密码部分可见性
        if self.MoneyLine.echoMode()==0:
            self.MoneyLine.setEchoMode(QtWidgets.QLineEdit.Password)
            return
        if self.MoneyLine.echoMode()==2:
            self.MoneyLine.setEchoMode(QtWidgets.QLineEdit.Normal)
            return
    
    def all_clear(self):    #清空全部行
        self.BigIntergerLine.clear()
        self.MoneyLine.clear()
        self.MyNameLine.clear()
        self.ResultLine.clear()
        self.Ten_Interger_Line.clear()
        self.The_j_th_num_Line.clear()
        self.WantNameLine.clear()
    
    def process(self):  #计算部分
        my_name=self.MyNameLine.text()
        want_name=self.WantNameLine.text()

        #简单的防止SQL注入过滤
        if 'AND' in want_name or '=' in want_name:
            self.action_fail.emit()

        money=self.MoneyLine.text()
        try:
            money=int(money)
        except:
            self.action_fail.emit()
            return
        if money<=0 or money>10:
            self.action_fail.emit()
            return
        
        try:
            res=client.SecureCompute_client(my_name,want_name,money)
        except:
            self.action_fail.emit()
            return

        result=res[0]
        bigint=res[1]
        res_dic=res[2]
        jth=res[3]
        self.BigIntergerLine.setText(str(bigint))
        string=""
        try:
            for i in range(10):
                string+=str(res_dic[i])
                string+="  "
        except:
            self.action_fail.emit()
            return
        self.Ten_Interger_Line.setText(string)
        self.The_j_th_num_Line.setText(str(jth))

        if result==True:
            res_string=u"您的财富小于或等于%s"%want_name
        elif result==False:
            res_string=u"您的财富大于%s"%want_name
        try:
            self.ResultLine.setText(res_string)
        except:
            self.action_fail.emit()
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = Millionaire_Dialog()
    window.show()
    sys.exit(app.exec_()) 

