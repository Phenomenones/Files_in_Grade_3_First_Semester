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
import time
import random
import threading
import pickle
import base64
import pyDes
import pymysql
import math

HOST = '0.0.0.0'
PORT = 10000
max_connection = 50
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

def Server_Transmit_Encrypt(s): #用客户端的公钥加密
    f=open('Public_Key/client-public.pem')
    Client_Public_Key=f.read()
    f.close()
    rsakey = RSA.importKey(Client_Public_Key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    num=int(len(s)/100)
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

def Server_Transmit_Decrypt(data): #用服务器的私钥解密
    f = open('Server_PrivateKey/server-private.pem')
    Server_Private_Key = f.read()
    f.close()
    random_generator = Random.new().read
    rsakey = RSA.importKey(Server_Private_Key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)

    length=len(data)
    res=b""
    for i in range(length):
        tmp=data[i]
        text = cipher.decrypt(base64.b64decode(tmp),random_generator)
        res += text
    return res  #不需要解码为UTF-8,因为pickle需要bytes作为输入而不是str！！！！！！！！！！！！

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
    message="This is from the Server with timestamp: "+str(ttt)
    f = open('Server_PrivateKey/server-private.pem')
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
    title=data[0:64]
    data=data[64:]
    hash_value=title

    sequence=data

    data = eval(data)
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
    f = open('Public_Key/client-public.pem')
    Client_Public_Key = f.read()
    f.close()
    rsakey = RSA.importKey(Client_Public_Key)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA256.new()
    m="This is from the Client with timestamp: "+str(timestamp)
    digest.update(m.encode("utf-8"))
    is_verify = verifier.verify(digest, base64.b64decode(siganture))
    if is_verify!=True:
        return False

    return data_dic #返回真正的数据部分

def mysql_manipulate(my_name,want_name,num):
    con = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='wangao970220',db='SecureComputation',charset='utf8',)
    cursor=con.cursor()
    
    #取回要比对的人的钱财数额
    sql='select money_value from account where name =\'%s\';'%want_name
    cursor.execute(sql)
    want_num=cursor.fetchall()
    if len(want_num)==0:
        con.close()
        return 'error'
    want_num=DES_decrypt(want_num[0][0].encode('utf-8'))
    con.close()
    return int(want_num)

def simple_RSA_decrypt(m):  #简单的RSA解密，用于使10个数字看起来完全随机
    N=2147483662032385529
    D=282476754508894175
    return pow(m,D,N)

def SecureCompute_server(data,client):  #i
    pair_dic = pickle.loads(data)

    my_name = pair_dic['my_name']
    num = pair_dic['num']
    want_name = pair_dic['want_name']

    print ('now receiving: %s'%my_name,', Address info: ',client.getpeername())
    x = mysql_manipulate(my_name,want_name,num);    #mysql
    if x=='error':
        return 'error'

    lis=[simple_RSA_decrypt(num+i) for i in range(10)]
    primes=[29,31,37,43,47]
    random.seed()
    index=random.randint(0,4)   #随机选择一个作为除数的质数
    p=primes[index]

    res_dic={}
    for i in range(10):
        res_dic[i]=lis[i]%p
    for i in range(x,10):
        res_dic[i] = (res_dic[i]+1)%p   #注意加1后要余p否则是错的！！！！！！！！！
    res_dic[10]=p   #包含10个数的字典的最后放入选择的作为除数的质数p

    res_dic=str(res_dic).encode("utf-8")
    ss = Server_Transmit_Encrypt(res_dic)

    ss=send_preprocessing(ss) #!!!

    client.send(str(ss).encode("utf-8"))

def handle(client, address):
    #预处理
    try:
        client.settimeout(TIMEOUT)
        data = client.recv(BUFFERSIZE)
        
        res=receive_pre_check(data) #!!!!!!
        if res==False:
            return

        #对真正的数据部分解密
        data = Server_Transmit_Decrypt(res)
        #开始算法核心部分
        res=SecureCompute_server(data,client)

    except timeout:
        print ('error: time out')
    client.close()

def main():
    path=sys.path[0]
    os.chdir(path)#get the current directory
    print ("start working...")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  
    sock.bind((HOST, PORT))  
    sock.listen(max_connection) 
    while True:  
        client,address = sock.accept()  
        thread = threading.Thread(target=handle, args=(client, address))    #每次接收都新建一个线程
        thread.start()
    sock.close()

if __name__  == "__main__":
    main()
