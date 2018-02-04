# -*- coding: utf-8 -*-

# Designed by WangAo, 15300240004

#输出结果图片到result文件夹

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

class ExtractWindow_Dialog(QDialog):
    def __init__(self,parent=None):
        super(ExtractWindow_Dialog,self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(680, 510)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(280, 50, 120, 120))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.HeightLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.HeightLine.setObjectName("HeightLine")
        self.HeightLine.setText('190')
        self.gridLayout.addWidget(self.HeightLine, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.LayerNumLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.LayerNumLine.setObjectName("LayerNumLine")
        self.LayerNumLine.setText('3')
        self.gridLayout.addWidget(self.LayerNumLine, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.WeightLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.WeightLine.setObjectName("WeightLine")
        self.WeightLine.setText('190')
        self.gridLayout.addWidget(self.WeightLine, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setRange(1,8)
        self.gridLayout.addWidget(self.spinBox, 3, 1, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(180, 20, 310, 30))
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
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 200, 200, 200))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MarkedImage = Image(self.verticalLayoutWidget)
        self.MarkedImage.setObjectName("MarkedImage")
        self.MarkedImage.setFixedSize(250,250)
        self.verticalLayout.addWidget(self.MarkedImage)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(320, 190, 30, 240))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(420, 200, 200, 200))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.WatermarkImage = QLabel(self.verticalLayoutWidget_2)
        self.WatermarkImage.setObjectName("WatermarkImage")
        self.WatermarkImage.setFixedSize(250,250)
        self.verticalLayout_2.addWidget(self.WatermarkImage)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(170, 450, 330, 30))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.OKButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.OKButton.setObjectName("OKButton")
        self.OKButton.setIcon(QtGui.QIcon('decorate/confirm.ico'))
        self.OKButton.clicked.connect(self.process)
        self.horizontalLayout_3.addWidget(self.OKButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.ClearButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.ClearButton.setObjectName("ClearButton")
        self.ClearButton.setIcon(QtGui.QIcon('decorate/empty.ico'))
        self.ClearButton.clicked.connect(self.clear)
        self.horizontalLayout_3.addWidget(self.ClearButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "抽取水印窗口"))
        self.label_4.setText(_translate("Dialog", "图层数："))
        self.label_3.setText(_translate("Dialog", "高："))
        self.label_2.setText(_translate("Dialog", "宽："))
        self.label_5.setText(_translate("Dialog", "比特位数："))
        self.label.setText(_translate("Dialog", "请输入要提取的水印图片的大小和提取位数："))
        self.MarkedImage.setText(_translate("Dialog", "Test"))
        self.WatermarkImage.setText(_translate("Dialog", "Test"))
        self.OKButton.setText(_translate("Dialog", "确认"))
        self.ClearButton.setText(_translate("Dialog", "清空"))

        file = QtCore.QFile('decorate/black_flat.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        file.close()

        self.ContainerURL="decorate/ImageWithMarkPrompt.png"
        self.WatermarkURL="decorate/WatermarkPrompt.png"

        pixmap=QtGui.QPixmap(self.ContainerURL).scaled(200, 200,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.MarkedImage.setPixmap(pixmap)
        pixmap=QtGui.QPixmap(self.WatermarkURL).scaled(200, 200,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.WatermarkImage.setPixmap(pixmap)

        self.MarkedImage.image_chose.connect(self.ContainerURL_receive)
    
    def clear(self):    #清空窗口，修改URL为默认URL
        self.LayerNumLine.setText('3')
        self.HeightLine.setText('190')
        self.WeightLine.setText('190')
        self.spinBox.setValue(1)

        self.ContainerURL="decorate/ImageWithMarkPrompt.png"
        self.WatermarkURL="decorate/WatermarkPrompt.png"

        pixmap=QtGui.QPixmap(self.ContainerURL).scaled(200, 200,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.MarkedImage.setPixmap(pixmap)
        pixmap=QtGui.QPixmap(self.WatermarkURL).scaled(200, 200,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.WatermarkImage.setPixmap(pixmap)

    def ContainerURL_receive(self,url): #收到包含水印图片的URL
        self.ContainerURL=url[start:]
        pixmap=QtGui.QPixmap(self.ContainerURL).scaled(200, 200,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.MarkedImage.setPixmap(pixmap)
    
    def process(self):  #开始提取过程
        a=int(self.WeightLine.text())
        b=int(self.HeightLine.text())
        layer=int(self.LayerNumLine.text())
        shape=(a,b,layer)
        site=int(self.spinBox.text())
        res=lsb.LSB_Extract(self.ContainerURL,shape,site)*255

        cv2.imwrite("result/watermark.bmp",res)
        self.WatermarkURL="result/watermark.bmp"
        pixmap=QtGui.QPixmap(self.WatermarkURL).scaled(200, 200,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.WatermarkImage.setPixmap(pixmap)


if __name__ == "__main__":
    path=sys.path[0]
    os.chdir(path)#get the current directory
    app = QApplication(sys.argv)    
    window = ExtractWindow_Dialog()
    window.show()
    sys.exit(app.exec_()) 