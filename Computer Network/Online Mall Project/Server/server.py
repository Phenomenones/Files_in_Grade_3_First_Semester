# -*- coding: utf-8 -*-

from socket import *
import json
import pyDes
import os
import sys
import time
import re
import threading

path=sys.path[0]
os.chdir(path)#get the current directory

HOST = '127.0.0.1'
PORT = 65432
HEADIMAGE_PORT = 65431  #登记新用户时发送头像的端口
KEY=b"i*k&y^t%" #DES算法密钥
BUFFERSIZE=2097152
TIMEINTERVAL = 5    #等待响应时间

def get_time_stamp():   #时间戳，防止重放攻击
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    timestamp = time.mktime(time_local)
    return timestamp

def encrypt(string):    #加密函数
    k = pyDes.des(KEY, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    return k.encrypt(string)

def decrypt(string):    #解密函数
    k = pyDes.des(KEY, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    return k.decrypt(string)

def identity_if_in_file(id,passw,url):  #获取登陆者信息,判断用户或者管理员是否存在
    file=open(url,"r")
    lines=file.readlines()
    file.close()
    flag=0
    res=""
    name=""
    ID=""
    for line in lines:
        line = line.replace('\r', '')
        ans=line.split("@")
        if len(ans) >= 4 and (id == ans[0] or id == ans[2]) and passw == ans[1]:    #姓名或者ID均可以
            flag=1
            ID=ans[0]
            name=ans[2]
            break
    return flag,ID,name

def login_handle(dic,address,s):    #处理登陆动作
    id=dic["id"]
    password=dic["password"]
    ans={}

    res=identity_if_in_file(id,password,"info/user.txt")
    
    if res[0] == 1:
        ans["state"]="succeed"
        ans["authority"]="user"
        ans["id"]=res[1]
        ans["name"]=res[2]
        ans = json.dumps(ans)
        ans=encrypt(ans)
        s.sendto(ans,address)
        return "succeed"
    
    res=identity_if_in_file(id,password,"info/admin.txt")
    
    if res[0] == 1:
        ans["state"]="succeed"
        ans["authority"]="admin"
        ans["id"]=res[1]
        ans["name"]=res[2]
        ans = json.dumps(ans)
        ans=encrypt(ans)
        s.sendto(ans,address)
        return "succeed"
    
    ans["state"]="fail"
    ans = json.dumps(ans)
    ans=encrypt(ans)
    s.sendto(ans,address)
    return "fail"
    
def headimage_handle(dic,address):    #处理用户头像请求
    '''
    jpg only
    '''
    s=socket(AF_INET,SOCK_DGRAM)    #新开一个用于传送头像的socket，减少主socket的负担
    path="info/image/"+dic["id"]+".jpg"
    with open(path, 'rb') as f:
        data = f.read(BUFFERSIZE)
        data=encrypt(data)
        s.sendto(data,address)
        #sudo sysctl -w net.inet.udp.maxdgram=65535 修改UDP缓冲区大小，才能上传图像
    s.close()

def shopinfo_handle(address,s): #处理获取商店请求
    file=open("info/shops.txt","r")
    lines=file.readlines()
    file.close()
    res={}
    i=0
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=3:
            tmp={}
            tmp["id"]=ans[0]
            tmp["shopname"]=ans[1]
            tmp["ownername"]=ans[2]
            res[i]=tmp
            i+=1
    res = json.dumps(res)
    res = encrypt(res)
    s.sendto(res,address)
    return
    
def messageinfo_handle(dic,address,s):  #处理获取消息请求
    file=open("info/messages.txt","r")
    lines=file.readlines()
    file.close()
    i=0
    res={}
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=5 and dic["id"] == ans[3] and dic["date1"]<=ans[0] and dic["date2"] >=ans[0]:  #还要判断时间
            tmp={}
            tmp["date"]=ans[0]
            tmp["time"]=ans[1]
            tmp["from"]=ans[2]
            tmp["content"]=ans[4]
            res[i]=tmp
            i+=1
    res = json.dumps(res)
    res = encrypt(res)
    s.sendto(res,address)
    return

def getgoods_handle(dic,address,s,good_num):    #处理获取商品请求
    file=open("info/goods.txt","r")
    lines=file.readlines()
    file.close()
    i=0
    res={}
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>= 4 and ans[2] == dic["shop_id"] and good_num.has_key(ans[0]):
            tmp={}
            tmp["good_id"]=ans[0]
            tmp["good_name"]=ans[1]
            tmp["price"]=ans[3]
            tmp["num"]=good_num[ans[0]]
            res[i]=tmp
            i+=1
    res = json.dumps(res)
    res = encrypt(res)
    s.sendto(res,address)
    return

def message_assemble(from_id,to_id,content):    #组装要写入messages.txt的详细信息
    file=open("info/messages.txt","a")
    time_ = list(time.localtime(time.time()))
    #日期
    string=str(time_[0])+'-'
    if len(str(time_[1]))==1:
        string+='0'
        string+=str(time_[1])
    else: string+=str(time_[1])
    string+="-"
    if len(str(time_[2]))==1:
        string+='0'
        string+=str(time_[2])
    else: string+=str(time_[2])
    string+="@"
    #时间
    if len(str(time_[3]))==1:
        string+='0'
        string+=str(time_[3])
    else: string+=str(time_[3])
    string+=":"
    if len(str(time_[4]))==1:
        string+='0'
        string+=str(time_[4])
    else: string+=str(time_[4])
    string+=":"
    if len(str(time_[5]))==1:
        string+='0'
        string+=str(time_[5])
    else: string+=str(time_[5])
    string+="@"
    #from_id
    string+=str(from_id)
    string+="@"
    #to_id
    string+=str(to_id)
    string+="@"
    #content
    string+=content
    string+="\n"
    return string

def register_new_good_handle(dic,address,s):    #登记新商品
    if str(dic["goodnum"]) == "":
        res={}
        res["state"]="fail"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)
        return
    file=open("info/goods.txt","r")
    lines=file.readlines()
    file.close()
    res={}
    flag=0
    good_id_list=[]#用来寻找最大值确定商品ID，商品ID为最大值加1
    res={}
    tmp=""
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=4:
            good_id_list.append(int(ans[0]))
            if ans[1] == dic["goodname"] and ans[2] == str(dic["shopid"]):
                flag=1
                tmp=ans[0]
    if flag==0: # 商品不存在
        string=str(max(good_id_list)+1)+"@"+dic["goodname"]+"@"+str(dic["shopid"])+"@"+str(float(dic["goodprice"]))+"\n"
        file=open("info/goods.txt","a")
        file.write(string)
        file.close()
        res["state"]="succeed"
    else: # 商品已经存在，不写回
        res["state"]="succeed"
    res = json.dumps(res)
    res = encrypt(res)
    s.sendto(res,address)
    if flag==0:
        ss=str(max(good_id_list)+1) #确定ID
    else: ss=tmp
    return ss

def if_shop_exists_handle(dic,address,s):   #判断用户商店是否存在
    user_id=dic["user_id"]
    file=open("info/shops.txt","r")
    lines=file.readlines()
    file.close()
    flag=0
    shop_name="none"
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if str(ans[0])==str(user_id):
            flag=1
            shop_name=ans[1]
    res={}
    res["shop_name"]=shop_name
    res = json.dumps(res)
    res = encrypt(res)
    s.sendto(res,address)

def broadcast_handle(dic,address,s,user_address):   #处理群发/广播消息情况
    if dic["content"]=="":  # 不许全部为空
        res={}
        res["state"]="fail"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)
        return
    file=open("info/user.txt","r")
    lines=file.readlines()
    file.close()
    users_id=[]
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=4:
            users_id.append(ans[0])
    for thing in users_id:
        from_id="root"
        to_id=str(thing)
        content=dic["content"]
        ss=message_assemble(from_id,to_id,content)
        file=open("info/messages.txt","a")
        file.write(ss)
        file.close()
    res={}
    res["state"]="succeed"
    res = json.dumps(res)
    res = encrypt(res)
    s.sendto(res,address)

def inform_handle(dic,address,s,user_address):  #处理单发消息情况
    file=open("info/user.txt","r")
    lines=file.readlines()
    file.close()
    users_id=[]
    flag=0
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=4 and str(dic["user_id"])==ans[0]:
            flag=1
    if flag==0:
        res={}
        res["state"]="fail"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)
        return
    else:
        from_id="root"
        to_id=str(dic["user_id"])
        content=dic["content"]
        ss=message_assemble(from_id,to_id,content)
        file=open("info/messages.txt","a")
        file.write(ss)
        file.close()
        res={}
        res["state"]="succeed"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)
        return

def get_all_user_handle(dic,address,s): #处理管理员获取全部用户请求
    file=open("info/user.txt","r")
    lines=file.readlines()
    file.close()
    users=[]
    user_shop=[]
    file=open("info/shops.txt","r")
    shops=file.readlines()
    file.close()
    for line in shops:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=3:
            user_shop.append(ans[0])
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        tmp={}
        if len(ans)>=4:
            if ans[0] in user_shop: #这个用户有商店
                id_=ans[0]+"*"  #有商店的用户特殊标记
            else:
                id_=ans[0]
            tmp["user_id"]=id_
            tmp["user_name"]=ans[2]
            users.append(tmp)
    users = json.dumps(users)
    users = encrypt(users)
    s.sendto(users,address)

def open_shop_handle(dic,address,s,user_address):   #处理开店请求
    file=open("info/shops.txt","r")
    lines=file.readlines()
    file.close()
    flag=1
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=3 and dic["user_id"]==ans[0]:  #商店已经存在,产生错误
            flag=0  #失败
    
    file=open("info/user.txt","r")
    lines=file.readlines()
    file.close()
    tag=0
    user_name=""
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=4 and dic["user_id"]==ans[0]:  #用户存在，才可以开通商店
            tag=1
            user_name=ans[2]
            break

    if flag==0 or tag==0:
        res={}
        res["state"]="fail"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)
        return
    else:
        file=open("info/shops.txt","a")
        string=dic["user_id"]+"@"+dic["shop_name"]+"@"+user_name+"\n"
        file.write(string)
        file.close()
        res={}
        res["state"]="succeed"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)
        #通知用户商店已开通
        from_id="root"
        to_id=str(dic["user_id"])
        content="Your Shop \"%s\" is now open, you can add products now!"%dic["shop_name"]
        ss=message_assemble(from_id,to_id,content)
        file=open("info/messages.txt","a")
        file.write(ss)
        file.close()
        return

def close_shop_handle(dic,address,s,user_address):  #处理关店请求
    file=open("info/shops.txt","r")
    lines=file.readlines()
    file.close()
    flag=0
    label=""
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=3 and dic["user_id"]==ans[0]:
            flag=1
            label = line
            break
    if flag==0: #商店不存在
        res={}
        res["state"]="fail"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)
        return
    else:
        new_file=open("info/new_file.txt","w")
        for line in lines:
            if label not in line:
                new_file.write(line)
        new_file.close()
        os.remove("info/shops.txt")
        os.rename(os.path.join("info","new_file.txt"),os.path.join("info","shops.txt"))
        res={}
        res["state"]="succeed"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)
    #通知用户商店已关闭
    from_id="root"
    to_id=str(dic["user_id"])
    content="Your Shop \"%s\" is closed."%dic["user_id"]
    ss=message_assemble(from_id,to_id,content)
    file=open("info/messages.txt","a")
    file.write(ss)
    file.close()
    return

def receive_headimage(address,new_id):  #用于在新的线程中收取头像
    #管理员只有一个,不会因同时上传头像而冲突
    ip=address[0]
    s=socket(AF_INET,SOCK_DGRAM)
    s.bind((ip,HEADIMAGE_PORT)) #使用接收头像的端口
    data,address = s.recvfrom(BUFFERSIZE)#接收头像
    data=decrypt(data)
    with open('info/image/%s.jpg'%str(new_id), 'ab') as f:  #写回数据
        f.write(data)
    s.close()
    return 

def register_new_user_handle(dic,address,s):    #登记新用户
    file=open("info/user.txt","r")
    lines=file.readlines()
    file.close()
    flag=1
    id_list=[]
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>=4:
            id_list.append(int(ans[0]))
        if len(ans)>=4 and dic["name"]==ans[2]:
            flag=0
    if flag==0: #重名，不允许发生
        res={}
        res["state"]="fail"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)
        ss="none"
        return ss
    else:
        res={}
        res["state"]="succeed"
        res = json.dumps(res)
        res = encrypt(res)
        s.sendto(res,address)

        new_id = max(id_list)+1 #新用户的ID为现有ID最大值加一

        t = threading.Thread(target=receive_headimage,args=(address,new_id))#创建线程
        t.setDaemon(True)#设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()#开启线程，接收头像

        file=open("info/user.txt","a")
        string=str(new_id)+"@"+dic["password"]+"@"+dic["name"]+"@"+"info/image/"+str(new_id)+".jpg"+"\n"
        file.write(string)
        file.close()
        ss=str(new_id)
        return ss

def get_newest_message_handle(dic,address,s,user_address):  #处理客户端额外的线程不断请求最新消息的请求
    timest = int(dic["timestamp"])
    file=open("info/messages.txt","r")
    lines=file.readlines()
    file.close()
    for i in range(len(lines)-1,-1,-1):
        line = lines[i]
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>= 5:
            dt = ans[0]+" "+ans[1]
            timeArray1 = time.strptime(dt, "%Y-%m-%d %H:%M:%S")

            time_local = time.localtime(timest)
            ts = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            timeArray2 = time.strptime(ts, "%Y-%m-%d %H:%M:%S")

            if int(ans[3]) == dic["user_id"] and timeArray1[0]==timeArray2[0] and timeArray1[1]==timeArray2[1] and timeArray1[2]==timeArray2[2] and timeArray1[3]==timeArray2[3] and timeArray1[4]==timeArray2[4] and abs(int(timeArray1[5]) - int(timeArray2[5])) <1:
                #将1秒内的最新消息返回
                res={}
                res["state"]="succeed"
                res["from_id"]= ans[2]
                res["content"] = ans[4]
                res = json.dumps(res)
                res = encrypt(res)
                s.sendto(res,address)
                return
    res={}
    res["state"]="fail"
    res = json.dumps(res)
    res = encrypt(res)
    s.sendto(res,address)
    return

def main():
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind((HOST,PORT))
    print 'start working...'

    good_num={} #当前商品的数量
    file=open("info/goods.txt","r")
    lines=file.readlines()
    file.close()
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>= 4:
            good_num.setdefault(ans[0],0)
            good_num[ans[0]]=5  #默认为5
    
    user_in_shop={} #当前店内用户
    file=open("info/user.txt","r")
    lines=file.readlines()
    file.close()
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>= 4:
            user_in_shop.setdefault(ans[0],"none")  #默认为none
    
    user_remain={} #用户余额
    file=open("info/user.txt","r")
    lines=file.readlines()
    file.close()
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>= 4:
            user_remain.setdefault(ans[0],500.0)    #默认为$500.0
    
    user_address={} #用户地址
    file=open("info/user.txt","r")
    lines=file.readlines()
    file.close()
    for line in lines:
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        ans=line.split("@")
        if len(ans)>= 4:
            user_address.setdefault(ans[0],("0.0.0.0",65355))   #考虑UDP的特性，初始地址任意选择

    while True:
        data,address = s.recvfrom(BUFFERSIZE)
        data = decrypt(data)
        if len(data)!=0:
            dic=eval(data)
        else:
            continue

        #防止重放攻击
        time1 = dic["timestamp"]
        time2 = get_time_stamp()
        if abs(time2 - time1) > TIMEINTERVAL:
            time1=0.0
            time2=0.0
            continue

        if dic["request"]=="login":
            ss = login_handle(dic,address,s)
            #仅在登录时设置user_address,退出时不用修改
            #因为UDP的特性，即使地址未开放，也可以发送消息
            #重新登录时可以更新用户地址
            user_address[dic["id"]] = address
        
        if dic["request"]=="headimage":
            headimage_handle(dic,address)

        if dic["request"]=="shopinfo":
            shopinfo_handle(address,s)
        
        if dic["request"]=="messageinfo":
            messageinfo_handle(dic,address,s)
        
        if dic["request"]=="getgoods":
            getgoods_handle(dic,address,s,good_num)
               
        if dic["request"]=="buygood":   #处理购买商品行为
            res={}
            if good_num.has_key(str(dic["good_id"])) and float(user_remain[dic["user_id"]])<=float(dic["good_price"]):
                res["state"]='fail'   #失败由余额不足引起
                res = json.dumps(res)
                res = encrypt(res)
                s.sendto(res,address)
                continue
            elif not good_num.has_key(str(dic["good_id"])):
                res={"num":0}
                res["state"]="succeed"
            elif good_num[str(dic["good_id"])] > 0:
                good_num[str(dic["good_id"])]-=1    #购买成功，商品数量减一
                res={"num":good_num[str(dic["good_id"])]}
                user_remain[dic["user_id"]]-=float(dic["good_price"])   #用户余额减去正确数值
                res["state"]="succeed"
            elif good_num[str(dic["good_id"])] == 0:    #商品购买完，则下架，删除
                del good_num[str(dic["good_id"])]
                res={"num":0}
                res["state"]="succeed"
            res = json.dumps(res)
            res = encrypt(res)
            s.sendto(res,address)
            
            #成功购买时才写入
            from_id="root"
            to_id=str(dic["shop_id"])
            content="User %s bought one %s(product ID) in your shop."%(dic["user_id"],dic["good_id"])
            ss=message_assemble(from_id,to_id,content)
            file=open("info/messages.txt","a")
            file.write(ss)
            file.close()
        
        if dic["request"]=="user_in_shop":  #发送用户进店消息
            user_in_shop[dic["user_id"]]=dic["shop_id"]

            from_id="root"
            to_id=str(dic["shop_id"])
            content="User %s went into your shop."%str(dic["user_id"])
            ss=message_assemble(from_id,to_id,content)
            file=open("info/messages.txt","a")
            file.write(ss)
            file.close()
       
        if dic["request"]=="get_customer_in_shop":  #获取当前店内用户
            res={}
            j=0
            for key in user_in_shop:
                if str(user_in_shop[key]) == str(dic["shop_id"]):
                    res[j]=key
                    j+=1
            res = json.dumps(res)
            res = encrypt(res)
            s.sendto(res,address)
        
        if dic["request"]=="user_leave_shop":   #发送用户离开商店消息
            user_in_shop[dic["user_id"]]="none"

            from_id="root"
            to_id=str(dic["owner_id"])
            content="User %s left your shop."%str(dic["user_id"])
            ss=message_assemble(from_id,to_id,content)
            file=open("info/messages.txt","a")
            file.write(ss)
            file.close()
        
        if dic["request"]=="register_new_good": #处理登记新货物
            ss=register_new_good_handle(dic,address,s)
            if str(dic["goodnum"]) != "":
                good_num.setdefault(ss,0)
                good_num[ss]=int(dic["goodnum"])
        
        if dic["request"]=="inform_new_good":   #通知商店内顾客有新商品上架
            file=open("info/messages.txt","a")
            cus_dic=dic["customer"]
            for key in cus_dic:
                from_id=str(dic["shop_id"])
                to_id=str(cus_dic[key])
                content="The shop %s you are in added product %s."%(str(dic["shop_id"]),str(dic["goodname"]))
                ss=message_assemble(from_id,to_id,content)
                file.write(ss)
            file.close()
        
        if dic["request"]=="if_shop_exists":    #判断用户是否有商店
            if_shop_exists_handle(dic,address,s)
        
        if dic["request"]=="get_user_remaining":    #获取用户余额
            res={}
            if str(dic["user_id"]) in user_remain:
                res["remaining"]=user_remain[str(dic["user_id"])]
                res["state"]="succeed"
            else:
                res["state"]="fail"
            res = json.dumps(res)
            res = encrypt(res)
            s.sendto(res,address)
        
        if dic["request"]=="charge_money":  #用户充钱
            user_remain[str(dic["user_id"])]+=float(dic["num"])
            res={}
            res["remaining"]=user_remain[str(dic["user_id"])]
            res = json.dumps(res)
            res = encrypt(res)
            s.sendto(res,address)
        
        if dic["request"]=="broadcast": #管理员对所有用户进行广播
            broadcast_handle(dic,address,s,user_address)
        
        if dic["request"]=="inform":    #通知单独的用户
            inform_handle(dic,address,s,user_address)
        
        if dic["request"]=="get_all_user":  #获得所有顾客信息
            get_all_user_handle(dic,address,s)
        
        if dic["request"]=="open_shop": #为用户开店
            open_shop_handle(dic,address,s,user_address)
        
        if dic["request"]=="close_shop":    #删除商店
            close_shop_handle(dic,address,s,user_address)
            #通知店内逛的用户该店已关闭
            file=open("info/messages.txt","a")
            cus_dic=dic["customer"]
            for key in cus_dic:
                from_id="root"
                to_id=str(cus_dic[key])
                content="The shop %s you are in is closed."%str(dic["user_id"])
                ss=message_assemble(from_id,to_id,content)
                file.write(ss)
            file.close()
        
        if dic["request"]=="register_new_user": #登记新用户
            ss=register_new_user_handle(dic,address,s)
            if ss != "none":    #处理用户余额和在商店位置
                user_in_shop.setdefault(ss,"none")
                user_remain.setdefault(ss,500.0)
                user_address.setdefault(ss,address)
        
        if dic["request"]=="get_newest_message":
            get_newest_message_handle(dic,address,s,user_address)
  
    s.close()

if __name__ == '__main__':
    main()