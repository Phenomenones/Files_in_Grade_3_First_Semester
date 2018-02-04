# -*- coding: utf-8 -*-

# Designed by WangAo, 15300240004

#输出图片到result文件夹

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
from PyQt5.QtGui import QMovie
import os
import sys
sys.path.append("LSB.py")
import LSB as lsb
import cv2

start = 8   #用于去掉“file://”头，URL的起始位置，Mac为7，Windows上为8

class Image(QLabel):   # 重载QLabel，方便拖拽式上传图片
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

class HideWindow_Dialog(QDialog):
    def __init__(self,parent=None):
        super(HideWindow_Dialog,self).__init__(parent)
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(830, 630)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(240, 40, 340, 20))
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
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(240, 70, 340, 20))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.spinBox = QtWidgets.QSpinBox(self.horizontalLayoutWidget_2)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setRange(1,8)
        self.horizontalLayout_2.addWidget(self.spinBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(390, 110, 40, 390))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget_3)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(240, 540, 340, 30))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.OKButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.OKButton.setObjectName("OKButton")
        self.OKButton.setIcon(QtGui.QIcon('decorate/confirm.ico'))
        self.OKButton.clicked.connect(self.process)
        self.horizontalLayout_4.addWidget(self.OKButton)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.ClearButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.ClearButton.setObjectName("ClearButton")
        self.ClearButton.setIcon(QtGui.QIcon('decorate/empty.ico'))
        self.ClearButton.clicked.connect(self.clear)
        self.horizontalLayout_4.addWidget(self.ClearButton)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(470, 180, 320, 270))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ResultImage = QLabel(self.horizontalLayoutWidget_5)
        self.ResultImage.setObjectName("ResultImage")
        self.ResultImage.setFixedSize(250,250)
        self.horizontalLayout_5.addWidget(self.ResultImage)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 80, 280, 450))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ContainerImage = Image(self.verticalLayoutWidget)
        self.ContainerImage.setObjectName("ContainerImage")
        self.ContainerImage.setFixedSize(220,220)
        self.verticalLayout.addWidget(self.ContainerImage)
        spacerItem88 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem88)
        self.WatermarkImage = Image(self.verticalLayoutWidget)
        self.WatermarkImage.setObjectName("WatermarkImage")
        self.WatermarkImage.setFixedSize(220,220)
        self.verticalLayout.addWidget(self.WatermarkImage)
        self.horizontalLayoutWidget.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.horizontalLayoutWidget_3.raise_()
        self.horizontalLayoutWidget_4.raise_()
        self.horizontalLayoutWidget_5.raise_()
        self.verticalLayoutWidget.raise_()
        self.OKButton.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "隐藏水印窗口"))
        self.label.setText(_translate("Dialog", "输入你要隐藏的bit位置 (1-8，1为最低位，8为最高位)："))
        self.OKButton.setText(_translate("Dialog", "确定"))
        self.ClearButton.setText(_translate("Dialog", "清空"))
        self.ResultImage.setText(_translate("Dialog", " 这里是包含水印的图片结果"))
        self.ContainerImage.setText(_translate("Dialog", "请将容器图片拖拽到这里"))
        self.WatermarkImage.setText(_translate("Dialog", "请将水印图片拖拽到这里"))

        self.ContainerImage.image_chose.connect(self.ContainerURL_receive)
        self.WatermarkImage.image_chose.connect(self.SecretURL_receive)

        self.ContainerURL="decorate/ContainerPrepImage.png"
        self.SecretURL="decorate/SecretPrepImage.png"
        self.MarkedURL="decorate/MarkedPrepImage.png"

        pixmap=QtGui.QPixmap(self.ContainerURL).scaled(220, 220, transformMode=QtCore.Qt.SmoothTransformation)
        self.ContainerImage.setPixmap(pixmap)
        pixmap=QtGui.QPixmap(self.SecretURL).scaled(220, 220, transformMode=QtCore.Qt.SmoothTransformation)
        self.WatermarkImage.setPixmap(pixmap)
        pixmap=QtGui.QPixmap(self.MarkedURL).scaled(250, 250, transformMode=QtCore.Qt.SmoothTransformation)
        self.ResultImage.setPixmap(pixmap)

        file = QtCore.QFile('decorate/black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()
    
    def clear(self):    #清空窗口，修改URL为默认URL
        self.ContainerURL="decorate/ContainerPrepImage.png"
        self.SecretURL="decorate/SecretPrepImage.png"
        self.MarkedURL="decorate/MarkedPrepImage.png"

        pixmap=QtGui.QPixmap(self.ContainerURL).scaled(220, 220, transformMode=QtCore.Qt.SmoothTransformation)
        self.ContainerImage.setPixmap(pixmap)
        pixmap=QtGui.QPixmap(self.SecretURL).scaled(220, 220, transformMode=QtCore.Qt.SmoothTransformation)
        self.WatermarkImage.setPixmap(pixmap)
        pixmap=QtGui.QPixmap(self.MarkedURL).scaled(250, 250, transformMode=QtCore.Qt.SmoothTransformation)
        self.ResultImage.setPixmap(pixmap)

        self.spinBox.setValue(1)
    
    def ContainerURL_receive(self,url): #收到容器图片的URL
        self.ContainerURL=url[start:]
        pixmap=QtGui.QPixmap(self.ContainerURL).scaled(220, 220,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.ContainerImage.setPixmap(pixmap)
    
    def SecretURL_receive(self,url):    #收到水印图片的URL
        self.SecretURL=url[start:]
        pixmap=QtGui.QPixmap(self.SecretURL).scaled(220, 220,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.WatermarkImage.setPixmap(pixmap)
    
    def process(self):  #开始隐藏过程
        site=int(self.spinBox.text())
        res=lsb.LSB_Hide(self.ContainerURL,self.SecretURL,site)
        cv2.imwrite("result/marked_%sbit.bmp"%str(self.spinBox.text()),res[0])
        self.MarkedURL="result/marked_%sbit.bmp"%str(self.spinBox.text())
        pixmap=QtGui.QPixmap(self.MarkedURL).scaled(250, 250,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.ResultImage.setPixmap(pixmap)
        

if __name__ == "__main__":
    path=sys.path[0]
    os.chdir(path)#get the current directory
    app = QApplication(sys.argv)    
    window = HideWindow_Dialog()
    window.show()
    sys.exit(app.exec_()) 