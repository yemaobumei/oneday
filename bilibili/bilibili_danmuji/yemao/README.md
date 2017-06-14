# play with bilibili
## 简介
* 模拟登陆bilibili弹幕网进行各类操作:接收弹幕，接入图灵机器人智能回复弹幕，礼物答谢,每日签到，小电视抽奖
* 哔哩哔哩 - ( ゜- ゜)つロ 乾杯~ - bilibili

## 安装说明
* 需要在python3环境下运行
* 需要安装以下库

```shell
sudo pip3 install bs4
sudo pip3 install requests
sudo pip3 install pycrypto
sudo pip3 install rsa
```

## 使用说明
* 首次运行请执行 login.py ，该脚本会进行登录操作并保存 cookies。
* 运行 danmuji.py 启动弹幕姬脚本,可实现在直播间自动答谢礼物，回复弹幕功能,并去小电视抽奖。
* 运行 dosign.py 开启每天自动签到功能，鉴于需要每天签到，可选择找一个服务器shell下后台执行
```shell
nohup python3 dosign.py > dosign.out 2>&1 &
```

## 计划实现功能 (三期)
* 实现进行小电视礼物抽奖，领取辣条银瓜子。

## 计划实现功能（二期）
* 接入图灵机器人智能回复弹幕
* 利用 aiohttp 实现异步发送弹幕
* dosign.py 加入每天自动签到功能，需要执行login.py登录之后才行

## 计划实现功能（一期）
* 实现websocket监听某直播间弹幕
* 根据自己设定的内容回复弹幕


本项目托管在[Github.com](https://github.com/yemaobumei/oneday/tree/master/bilibili/bilibili_danmuji)中