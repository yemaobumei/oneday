#!/usr/bin/python3
#coding=utf-8
import requests
import time

#获取直播流地址:cid=roomid
"http://live.bilibili.com/api/playurl?player=1&cid=1273106&quality=0"


#24小时挂直播
"http://api.live.bilibili.com/feed/v1/feed/heartBeat" 
result = {"code":0,"msg":"success","message":"success","data":{"count":9,"open":1,"has_new":1}}

"http://api.live.bilibili.com/User/userOnlineHeart"
result = {"code":0,"msg":"","data":[]}

"http://api.live.bilibili.com/eventRoom/heart?roomid=80397"
result = {"code":-403,"msg":"\u9886\u53d6\u5931\u8d25","data":{"heart":true}}

##获取粉丝列表
url = "http://space.bilibili.com/ajax/friend/GetFansList"
params = {'mid':uid,'page':page,'_':int(time.time()*1000)}
s = requests.session()
s.trust_env = False
s.get(url,params=params).json()

#获取直播间直播流地址
roomid = '2570641'
url = "http://api.live.bilibili.com/api/playurl"
params = {'platform':'h5','cid':roomid} #获取H5播放地址
params = {'cid':roomid} #普通flash播放地址
result=s.get(url,params=params).text

#好像失效了
# #获取用户信息
# #通过用户昵称获取
# name = "最短的夜猫"
# url = 'http://api.bilibili.cn/userinfo'+"?user="+name
# url = 'http://api.bilibili.cn/userinfo'+"?mid="+mid

var DMPORT = 2243;
var DMSERVER = 'livecmt-2.bilibili.com';

var WSDMPROTOCOL = 'ws';
var WSSDMPROTOCOL = 'wss';
var WSDMSERVER = 'broadcastlv.chat.bilibili.com';
var WSDMPORT = 2244;
var WSSDMPORT = 2245;
var WSDMPATH = 'sub';

var HEARTBEAT_DELAY = 1e4;
var GIFT_END_DELAY = 3e3;
var FETCH_FANS_DELAY = 5e3;
var CHECK_DELAY = 15e3;
this.socket = new WebSocket(`${WSDMPROTOCOL}://${WSDMSERVER}:${WSDMPORT}/${WSDMPATH}`)
""
