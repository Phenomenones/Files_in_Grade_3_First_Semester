# -*- coding: utf-8 -*-

# 王傲  15300240004
# 使用Let It Crash原则 

import cv2
import numpy as np
import sys
import os

def bitset(num,site,bit):   #将num的第site位置为bit
    num=int(num)
    site=int(site)
    bit=int(bit)
    if bit!=1 and bit!=0:
        return
    tmp=bin(num)
    tmp=tmp[2:]
    if site>len(tmp):
        if bit == 0:
            return num
        else:
            n=2**(site-1)
            return n+num
    else:
        lo=len(tmp)-site
        tmp=tmp[:lo]+str(bit)+tmp[lo+1:]
        return int(tmp,2)

def img2lis(img_path):  #将图像转换为比特串
    image=cv2.imread(img_path)
    shape=image.shape
    a=shape[0]
    b=shape[1]
    layer_num=shape[2]
    lis=''
    for layer in range(layer_num):
        for i in range(a):
            for j in range(b):
                tmp=image[i,j,layer]
                tmp=bin(tmp)
                tmp=tmp[2:]
                ll=len(tmp)
                for iterator in range(8-ll):
                    tmp='0'+tmp
                lis+=tmp
    return lis

def LSB_Hide(container_path,secret_path,site):  #实现隐藏算法
    container=cv2.imread(container_path)
    secret=cv2.imread(secret_path)

    shape=secret.shape
    length=shape[0] * shape[1] * shape[2] * 8   
    lis=img2lis(secret_path)

    a=container.shape[0]
    b=container.shape[1]
    layer=container.shape[2]

    flag1=0
    flag2=0
    record=0
    for layer in range(layer):  #按顺序，逐个字节的隐藏bit
        for i in range(a):
            for j in range(b):
                if record < length:
                    tmp=container[i,j,layer]
                    tmp=bitset(tmp,site,int(lis[record]))   #根据输入的位置替换相应比特
                    container[i,j,layer]=tmp
                else:
                    flag1=1
                    break
                record+=1
            if flag1==1:
                flag2=1
                break
        if flag2==1:
            break        
    return container,shape

def LSB_Extract(marked_path,secret_shape,site): #实现提取算法
    container=cv2.imread(marked_path)
    length=secret_shape[0] * secret_shape[1] * secret_shape[2] * 8

    secret=np.zeros((secret_shape[0],secret_shape[1],secret_shape[2]))

    a=container.shape[0]
    b=container.shape[1]
    layer=container.shape[2]

    flag1=0
    flag2=0
    record=0
    lis=''
    for layer in range(layer):  #按顺序，逐个字节的提取bit
        for i in range(a):
            for j in range(b):
                if record < length:
                    tmp=container[i,j,layer]
                    tmp=bin(tmp)
                    tmp=tmp[2:]
                    ll=len(tmp)
                    for iterator in range(8-ll):
                        tmp='0'+tmp
                    bit=tmp[8-site] #提取出对应位置的比特
                    lis+=bit
                else:
                    flag1=1
                    break
                record+=1
            if flag1==1:
                flag2=1
                break
        if flag2==1:
            break  
    
    for layer in range(secret_shape[2]):
        for i in range(secret_shape[0]):
            for j in range(secret_shape[1]):
                tmp=lis[0:8]
                lis=lis[8:]
                secret[i,j,layer]=int(tmp,2)
    return secret/255.0

if __name__ == "__main__":
    path=sys.path[0]
    os.chdir(path)#get the current directory
    a="fudan.bmp"
    b="image.bmp"

    bit=1

    original_watermark = cv2.imread(b)

    res=LSB_Hide(a,b,bit)
    cv2.imwrite("marked.bmp",res[0])
    c="marked.bmp"
    result=LSB_Extract(c,res[1],bit)

    cv2.imshow("Image", result)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

    '''mat=np.zeros((10,8)) #获取LSB存储在不同bit位置下的差异率

    for quality in range(10,110,10):
        for bit in range(1,9):

            original_watermark = cv2.imread(b)

            res=LSB_Hide(a,b,bit)
            cv2.imwrite("marked.jpg",res[0],[int(cv2.IMWRITE_JPEG_QUALITY),quality])
            c="marked.jpg"
            result=LSB_Extract(c,res[1],bit)


            changed_watermark=result*255.0

            different=0
            layer_num=res[1][2]
            x=res[1][0]
            y=res[1][1]

            for layer in range(layer_num):
                for i in range(x):
                    for j in range(y):
                        tmp1=original_watermark[i,j,layer]
                        tmp1=bin(tmp1)
                        tmp1=tmp1[2:]

                        tmp2=changed_watermark[i,j,layer]
                        tmp2=bin(int(tmp2))
                        tmp2=tmp2[2:]
                        le1=len(tmp1)
                        le2=len(tmp2)
                        for ii in range(8-le1):
                            tmp1='0'+tmp1
                        for ii in range(8-le2):
                            tmp2='0'+tmp2
                        bit1=tmp1[8-bit]
                        bit2=tmp2[8-bit]
                        if bit1!=bit2:
                            different+=1
            res=float(different)/float(res[1][0]*res[1][1]*res[1][2])
            mat[(quality/10)-1,bit-1]=res
    print mat'''

