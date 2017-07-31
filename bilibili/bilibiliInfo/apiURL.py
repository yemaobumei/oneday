#!/usr/bin/python3
#coding=utf-8
import requests
import time


# 手机请求头
# CONNECT message.bilibili.com:443 HTTP/1.1
# Host: message.bilibili.com
# User-Agent: bili-universal/5960 CFNetwork/808.3 Darwin/16.3.0
# Connection: keep-alive
# Proxy-Connection: keep-alive

#获取直播流地址:cid=roomid
"http://live.bilibili.com/api/playurl?player=1&cid=1273106&quality=0"


#24小时挂直播
"http://api.live.bilibili.com/feed/v1/feed/heartBeat" 
result = {"code":0,"msg":"success","message":"success","data":{"count":9,"open":1,"has_new":1}}

"http://api.live.bilibili.com/User/userOnlineHeart"
result = {"code":0,"msg":"","data":[]}

"http://api.live.bilibili.com/eventRoom/heart?roomid=80397"
result = {"code":-403,"msg":"\u9886\u53d6\u5931\u8d25","data":{"heart":true}}



##直播间信息
url="http://api.live.bilibili.com/live/getInfo"
params={'roomid':roomid}
result={'code': 0, 'msg': 'OK', 'data': {'UID': 0, 'UNAME': 0, 'IS_NEWBIE': 1, 'ISADMIN': 0, 'ISANCHOR': 0, 'ISPHONE': 0, 'SILVER': 0, 'GOLD': 0, 'SVIP': 0, 'VIP': 0, 'USER_LEVEL': [], 'FANS_COUNT': 21245, 'ISATTENTION': 0, 'ROOM_SILENT_TYPE': 0, 'ROOM_SILENT_LEVEL': 0, 'ROOM_SILENT_SECOND': 0, 'BLOCK_TYPE': 0, 'BLOCK_TIME': 0, 'RCOST': 4707032, 'SAN': 12, 'MASTERID': 6383587, 'ANCHOR_NICK_NAME': '喵咭喵呜', 'ROOMID': 1273106, '_status': 'on', 'LIVE_STATUS': 'LIVE', 'ROUND_STATUS': 1, 'AREAID': 6, 'BACKGROUND_ID': 6, 'ROOMTITLE': '请和废柴的我做朋友吧&amp;gt;&amp;lt;!!', 'COVER': 'http://i0.hdslb.com/bfs/live/1273106.jpg?07302236', 'LIVE_TIMELINE': 1501413864, 'GIFT_TOP': [], 'MEDAL': [], 'TITLE': {'title': ''}, 'IS_RED_BAG': False, 'IS_HAVE_VT': False, 'ACTIVITY_ID': 0, 'ACTIVITY_PIC': 0, 'GUARD': 0, 'GUARD_INFO': {'heart_status': True, 'heart_time': 300, 'notice_status': 0, 'water_god': 0}, 'PENDANT': '', 'AREAPENDANT': '', 'IS_STAR': False, 'starRank': 0, 'MI_ACTIVITY': 0, 'MUSUME': '22'}}

#获取直播间直播流地址
roomid = '2570641'
url = "http://api.live.bilibili.com/api/playurl"
params = {'platform':'h5','cid':roomid} #获取H5播放地址
params = {'cid':roomid} #普通flash播放地址
result=s.get(url,params=params).text

##历史弹幕
url="http://api.live.bilibili.com/ajax/msg"
data={'roomdi':roomid}
s.post(url,data=data)

##获取粉丝列表
url = "http://space.bilibili.com/ajax/friend/GetFansList"
params = {'mid':uid,'page':page,'_':int(time.time()*1000)}
s = requests.session()
s.trust_env = False
s.get(url,params=params).json()

##房管列表
url="http://api.live.bilibili.com/liveact/ajaxGetAdminList"
data={'roomid':roomid}
s.post(url,data=data)

##直播间被禁用户列表,需要登录的cookie
url="http://api.live.bilibili.com/liveact/ajaxGetBlockList"
data={'roomid':roomid}
s.post(url,data=data)
result={'code': 0, 'msg': '', 'data': [{'id': 1060846, 'roomid': 80397, 'uid': 30835251, 'type': 1, 'block_end_time': '2017-08-29 18:19:06', 'ctime': '2017-07-30 18:19:06', 'adminid': 32388051, 'uname': '假寐十年', 'admin_uname': '夏风风风'}]}

##禁言用户,需要登录ookie
url="http://api.live.bilibili.com/liveact/room_block_user"
data={'roomid':roomid,'content':userId,type:1,hour:hour}

##取消禁言用户
url="api.live.bilibili.com/liveact/del_room_block_user"
data={'roomid':roomid,'id':blockid}

##管理房管
url="http://api.live.bilibili.com/liveact/admin"
data={'roomid':roomid,'content':userId,'type':'add'}
data={'roomid':roomid,'content':userId,'type':'del'}

##在线心跳
url="http://api.live.bilibili.com/User/userOnlineHeart"
method="POST"
s.post(url)

##礼物心跳
url="http://api.live.bilibili.com/eventRoom/heart"
params={'roomid':roomid}
s.get(url,params=params)

##小电视参与
url="http://api.live.bilibili.com/SmallTV/join"

s.post(url,data=data)

api.live.bilibili.com/SmallTV/getReward

##每日签到
url="http://api.live.bilibili.com/sign/doSign"
