#!/bin/bash

#获取直播流地址
roomid="1273106"
live_info=$(curl "http://live.bilibili.com/api/playurl?player=1&cid=${roomid}&quality=0"|grep b1url)
live_url=$(echo $live_info|cut -d '[' -f 3|cut -d ']' -f 1)

#循环推送直播流
while true
do
status=$(curl "http://api.live.bilibili.com/live/getInfo?roomid=${roomid}"|sed -e 's/[{}]/''/g'|awk -v RS=',"' -F: '/^_status/{print $2}')
#if [[ $live_info =~ 'CDATA' ]]

#解析json数据，判断是否正在直播
#curl http://api.live.bilibili.com/live/getInfo?roomid=80397 |sed -e 's/[{}]/''/g'|awk -v RS=',"' -F: '/^_status/{print $2}'
#curl http://api.live.bilibili.com/live/getInfo?roomid=80397 |python3 -c 'import json,sys;obj=json.load(sys.stdin);print(obj["data"]["_status"])'

#判断是否正在直播
if [[ $status =~ "on" ]]
then
	ffmpeg -re -i "$live_url" -vcodec copy -acodec aac -b:a 100k -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"  
else
	ffmpeg -re -i "miao4_2_x264.mp4" -vcodec copy -acodec aac -b:a 128k -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"
fi
done

