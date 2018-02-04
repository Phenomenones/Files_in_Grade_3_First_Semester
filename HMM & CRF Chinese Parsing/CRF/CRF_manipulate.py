# -*- coding:utf-8 -*- 
#Author: Ao Wang, 15300240004

#a simple example to show how to segment

from sklearn.externals import joblib
import os
import sys
sys.path.append("CRF.py")
import CRF

path=sys.path[0]
os.chdir(path)#get the current directory

la=joblib.load("CRF_8e6.pkl") 
print "CRF loaded"


s="韦恩夫妇遇害后，深受信赖的阿尔弗莱德就成了布鲁斯的监护人。"
res=CRF.partition(s,la)
for thing in res:
    print thing