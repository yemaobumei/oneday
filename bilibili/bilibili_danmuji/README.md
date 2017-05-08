# play with bilibili
## 简介
* 模拟登陆bilibili弹幕网进行各类操作:接收弹幕，发送弹幕，接入图灵机器人
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
* 首次运行请执行main.py，该脚本会进行登录操作并保存cookies和登录状态，启动弹幕姬脚本。



## 计划实现功能（二期）
* 接入图灵机器人智能回复弹幕
* 利用aiohttp实现异步发送弹幕


## 计划实现功能（一期）
* 实现websocket监听某直播间弹幕
* 根据自己设定的内容回复弹幕


本项目同时托管在[Github.com](https://github.com/ookcode/BilibiliSofaSitter)与[Coding.net](https://coding.net/u/ookcode/p/bilibili/git)中