# -*- coding:utf-8 -*-  
#Author: Ao Wang, 15300240004

#a simple example to show how to segment

import sys
sys.path.append('HMM.py')
import os

import pickle
import HMM

path=sys.path[0]
os.chdir(path)#get the current directory

file1=open("InitiateProb.pkl","r")
file2=open("TransProbMatrix.pkl","r")
file3=open("EmitProbMatrix.pkl","r")

a=pickle.load(file1)
b=pickle.load(file2)
c=pickle.load(file3)

file1.close()
file2.close()
file3.close()



sen="韦恩夫妇遇害后，深受信赖的阿尔弗莱德就成了布鲁斯的监护人。"
res=HMM.partition(sen,a,b,c)


for thing in res:
    print thing
