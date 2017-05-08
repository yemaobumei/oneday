#!/usr/bin/python3
#coding=utf-8

from api import Client

#登录B站获取cookies
username=input('请输入用户名: ')
password=input('请输入密码: ')
LoginClient=Client(username,password)
cookies=LoginClient.cookies_login()
while not LoginClient.isLogin:
	LoginClient.login()
	if LoginClient.isLogin:
		break
print('登录成功',username)