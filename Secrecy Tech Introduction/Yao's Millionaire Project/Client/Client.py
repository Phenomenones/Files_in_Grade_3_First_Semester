# -*- coding: utf-8 -*-
# Designed by Wang Ao, 15300240004

from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

import sys
import os
from socket import *
import random
import pickle
import base64
import time
import fractions
import math
import pyDes

HOST = '0.0.0.0'#'182.254.130.132'#'0.0.0.0'
PORT = 10000
TIMEOUT = 500
BUFFERSIZE = 32768
TIMEINTERVAL = 5    #等待响应时间
KEY=b"i*k&y^t%" #DES算法密钥

def DES_encrypt(string):    #数据库加密函数
    k = pyDes.des(KEY, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    return base64.b64encode(k.encrypt(string))

def DES_decrypt(string):    #数据库解密函数
    k = pyDes.des(KEY, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    return k.decrypt(base64.b64decode(string))

def Client_Transmit_Encrypt(s): #用服务器的公钥加密
    f=open('Public_Key/server-public.pem')
    Server_Public_Key=f.read()
    f.close()
    rsakey = RSA.importKey(Server_Public_Key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)

    num=int(len(s)/100) #采用1024bit的密钥，分块大小为100bit
    if len(s)%100>0:
        num+=1
    tmp=s
    res={}
    for i in range(num-1):
        string=tmp[0:100]
        tmp=tmp[100:]
        res[i]=base64.b64encode(cipher.encrypt(string))
    res[num-1]=base64.b64encode(cipher.encrypt(tmp[:]))
    return res

def Client_Transmit_Decrypt(data): #用客户端的私钥解密
    f = open('Client_PrivateKey/client-private.pem')
    Client_Private_Key = f.read()
    f.close()
    random_generator = Random.new().read
    rsakey = RSA.importKey(Client_Private_Key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    length=len(data)
    res=b""
    for i in range(length): #将拆开的块拼接起来
        tmp=data[i]
        text = cipher.decrypt(base64.b64decode(tmp),random_generator)
        res += text
    return res  #不需要解码，但不是因为pickle，而是后面一起解码，防止UTF-8字符被拆开导致无法解析！！！！！！！

def get_time_stamp():   #时间戳，防止重放攻击
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    timestamp = time.mktime(time_local)
    return timestamp

def send_preprocessing(data_dic):
    #安全通信部分，字典第一部分是数据，第二部分是时间戳，第三部分是签名
    send_dic={}
    send_dic[1]=data_dic
    ttt=get_time_stamp()
    send_dic[2]=DES_encrypt(str(ttt))

    #签名内容：固定字符串+时间戳
    message="This is from the Client with timestamp: "+str(ttt)
    f = open('Client_PrivateKey/client-private.pem')
    Client_Private_Key = f.read()
    f.close()
    rsakey = RSA.importKey(Client_Private_Key)
    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(message.encode("utf-8"))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    send_dic[3]=signature

    #加上SHA256校验
    #校验内容：字典部分的内容加时间戳
    ss=str(send_dic)
    digest = SHA256.new()
    tmp=ss+str(ttt) #加盐，即时间戳，防止攻击者修改字典部分再反过来计算SHA256的值
    digest.update(tmp)
    title=digest.hexdigest() #length: 64
    ss=title+ss #!!!!!!!!加在头部，SHA256校验长为64
    return ss

def receive_pre_check(data):
    data = data.decode("utf-8")

    #先获得头部的SHA256校验
    title=data[0:64]    #头部的校验部分
    data=data[64:]  #数据部分
    hash_value=title
    sequence=data

    try:
        data = eval(data)
    except:
        return False
    data_dic=data[1]    #获得加密的数据字典
    timestamp = float(DES_decrypt(data[2])) #获得时间戳
    time2 = get_time_stamp()
    if abs(time2 - timestamp) > TIMEINTERVAL:   #超过时间则拒绝服务
        return False
    siganture=data[3]   #获得签名

    #计算SHA256校验是否正确
    sequence=sequence+str(timestamp)
    digest = SHA256.new()
    digest.update(sequence)
    if digest.hexdigest()!=hash_value:
        return False
        
    #计算签名是否正确
    f = open('Public_Key/server-public.pem')
    Client_Public_Key = f.read()
    f.close()
    rsakey = RSA.importKey(Client_Public_Key)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA256.new()
    m="This is from the Server with timestamp: "+str(timestamp)
    digest.update(m.encode("utf-8"))
    is_verify = verifier.verify(digest, base64.b64decode(siganture))
    if is_verify!=True:
        return False

    return data_dic #返回真正的数据部分

def lcm(a,b): #最小公倍数
    return int(abs(a * b) / fractions.gcd(a,b) if a and b else 0)

def simple_RSA_encrypt(m):  #用于计算部分的简单RSA，目的是使十个数字看起来完全随机
    N=2147483662032385529
    E=314159
    return pow(m,E,N)
    
def SecureCompute_client(my_name,want_name,y):  #j
    path=sys.path[0]
    os.chdir(path)#get the current directory

    #设立TCP socket
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(TIMEOUT)
    s.connect((HOST,PORT))
    
    random.seed()
    x = random.randint(200000,300000)
    bigint=x

    K = simple_RSA_encrypt(x)
    num=K-y+1

    #协议部分
    pair_dic={}
    pair_dic['my_name']=my_name
    pair_dic['num']=num
    pair_dic['want_name']=want_name
    data_dic = Client_Transmit_Encrypt(pickle.dumps(pair_dic))
    ss=send_preprocessing(data_dic) #!!!
    s.send(str(ss).encode("utf-8"))

    ss = s.recv(BUFFERSIZE)
    ss = receive_pre_check(ss) #!!!!!!
    if ss == False:
        return "error"
    #发送部分
    res_dic = Client_Transmit_Decrypt(ss)
    res_dic = res_dic.decode("utf-8")
    res_dic = eval(res_dic)
    s.close()

    #算法核心部分
    try:
        num=res_dic[y-1]
    except:
        return 'error'
    p=res_dic[10]   #包含10个数的字典的最后放入对方选择的作为除数的质数p
    if num == x%p:
        result = True     #"x >= y"
    else:
        result = False    #"x < y"
    
    return result,bigint,res_dic,res_dic[y-1]

if __name__ == "__main__":
    path=sys.path[0]
    os.chdir(path)#get the current directory
    #a= SecureCompute_client('Bob','Alice',7)    #y
    #print (a[0])
    it=0
    flag=0
    #测试部分
    for i in range(100):
        it+=1
        random.seed()
        y = random.randint(1,10)
        #print (y)
        res = SecureCompute_client('Bob','Alice2',y)    #!!!!
        if (2 >= y and res[0]==True) or (2 < y and res[0]==False):
            flag+=1
    print ('总共测试数目： '+str(it))
    print ('正确数目： '+str(flag))