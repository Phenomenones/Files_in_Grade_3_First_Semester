# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HMM_GUI.ui'
# Created by: PyQt5 UI code generator 5.9.2
# WARNING! All changes made in this file will be lost!

#Created by Ao Wang, 15300240004

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
import os
import sys
sys.path.append('HMM.py')
import pickle
import HMM

class Ui_Dialog(QDialog):
    def __init__(self,parent=None):
        super(Ui_Dialog,self).__init__(parent)
        self.setupUi(self)

        self.path=sys.path[0]
        os.chdir(self.path)#get the current directory
        self.file1=open("InitiateProb.pkl","r")
        self.file2=open("TransProbMatrix.pkl","r")
        self.file3=open("EmitProbMatrix.pkl","r")

        self.InitiateProb=pickle.load(self.file1)
        self.TransProbMatrix=pickle.load(self.file2)
        self.EmitProbMatrix=pickle.load(self.file3)

        self.file1.close()
        self.file2.close()
        self.file3.close()
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(670,350)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 20, 630, 310))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.GUI_Name = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.GUI_Name.setObjectName("GUI_Name")
        self.horizontalLayout_3.addWidget(self.GUI_Name)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TipLine1 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.TipLine1.setObjectName("TipLine1")
        self.horizontalLayout.addWidget(self.TipLine1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.InputText = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.InputText.setObjectName("InputText")
        self.verticalLayout.addWidget(self.InputText)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.TipLine2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.TipLine2.setObjectName("TipLine2")
        self.horizontalLayout_2.addWidget(self.TipLine2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.OutputText = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.OutputText.setObjectName("OutputText")
        self.OutputText.setReadOnly(True)
        self.verticalLayout_2.addWidget(self.OutputText)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.StartButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.StartButton.setObjectName("StartButton")
        self.StartButton.clicked.connect(self.partition)
        self.horizontalLayout_4.addWidget(self.StartButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.ClearButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.ClearButton.setObjectName("ClearButton")
        self.ClearButton.clicked.connect(self.clear)
        self.horizontalLayout_4.addWidget(self.ClearButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "HMM Segmentor GUI"))
        self.GUI_Name.setText(_translate("Dialog", "HMM Segmentor GUI"))
        self.TipLine1.setText(_translate("Dialog", "Please input your sentence here (one at a time):"))
        self.TipLine2.setText(_translate("Dialog", "The partition results:"))
        self.StartButton.setText(_translate("Dialog", "Start"))
        self.ClearButton.setText(_translate("Dialog", "Clear"))
    
    def partition(self):
        '''
        Segment the sentence in the showing window
        '''
        sen=self.InputText.toPlainText()
        sen=sen.encode("utf8")
        res=HMM.partition(sen,self.InitiateProb,self.TransProbMatrix,self.EmitProbMatrix)
        stri=""
        for thing in res:
            stri+=thing
            stri+="  "
        #stri=stri.decode("utf8")
        stri=stri[0:len(stri)-1]
        self.OutputText.setText(stri)
        return None

    def clear(self):
        '''
        Clear the window
        '''
        self.InputText.setText("")
        self.OutputText.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = Ui_Dialog()
    window.show()
    sys.exit(app.exec_()) 