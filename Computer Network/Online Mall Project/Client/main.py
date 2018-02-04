# -*- coding: utf-8 -*-

#Designed by Ao Wang, 15300240004

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
import os
import sys
from socket import *
import json
sys.path.append("IP.py")
sys.path.append("Login.py")
sys.path.append("UserInterface.py")
sys.path.append("GoodsList.py")
sys.path.append("MyShop.py")
sys.path.append("AdminInterface.py")
sys.path.append("Admin_GoodsList.py")
sys.path.append("NewUser.py")
import IP as ip
import Login as login
import UserInterface as ui
import GoodsList as gl
import MyShop as ms
import AdminInterface as ai
import Admin_GoodsList as ag
import NewUser as nu

def main():
    app = QApplication(sys.argv)
    path=sys.path[0]
    os.chdir(path)#get the current directory
    
    #initialize the objects
    login_win = login.Login_Dialog()
    error_win = ip.Error_Dialog()
    userinterface_win = ui.Userinterface_Dialog()
    goodslist_win = gl.GoodsList_Dialog()
    customerlist_win = gl.CustomerList_Dialog()
    myshop_win = ms.MyShop_Dialog()
    admininterface_win = ai.Admininterface_Dialog()
    admin_customerlist_win = ag.Admin_CustomerList_Dialog()
    admin_goodslist_win = ag.Admin_GoodsList_Dialog()
    newuser_win = nu.NewUser_Dialog()

    
    #connect the signal

    #user part
    login_win.login_fail.connect(error_win.show_myself)#操作失败时显示提示窗口
    login_win.login_succeed_user.connect(userinterface_win.receive_user_argument)#用户登陆成功，打开用户界面
    userinterface_win.this_hide.connect(login_win.show_myself)#退出用户界面时返回登陆界面
    userinterface_win.shop_chose.connect(goodslist_win.receive_info)#用户选择商店后打开该商店窗口
    goodslist_win.cus_list.connect(customerlist_win.reveice_data)#用户查看当前店内顾客时打开顾客列表
    goodslist_win.exit_shop.connect(userinterface_win.user_leave_shop)#用户退出商店时发送退出信号
    userinterface_win.myshop.connect(myshop_win.get_owner)#用户进入 我的商店 时打开自己商店的界面
    myshop_win.act_fail.connect(error_win.show_myself)#用户创建新商品失败时显示提示窗口
    userinterface_win.act_fail.connect(error_win.show_myself)#用户充值失败时显示提示窗口
    goodslist_win.act_fail.connect(error_win.show_myself)#余额不足时显示提示窗口
    goodslist_win.remain_update.connect(userinterface_win.get_remaining)#买东西后提醒更新余额窗口


    #admin part
    login_win.login_succeed_admin.connect(admininterface_win.receive_admin_argument)#管理员登陆成功，打开管理员界面
    admininterface_win.this_hide.connect(login_win.show_myself)#退出管理员界面时返回登录界面
    admininterface_win.act_fail.connect(error_win.show_myself)#操作失败时显示提示窗口
    admininterface_win.shop_chose.connect(admin_goodslist_win.receive_info)#管理员选择商店后打开该商店窗口
    admin_goodslist_win.cus_list.connect(admin_customerlist_win.reveice_data)#管理员查看当前店内顾客时打开顾客列表
    admininterface_win.new_user.connect(newuser_win.show_win)#点击创建用户按钮，打开窗口
    newuser_win.act_fail.connect(error_win.show_myself)#操作失败时显示提示窗口

    login_win.show()
    sys.exit(app.exec_())
    
    
if __name__ == "__main__":
     main()