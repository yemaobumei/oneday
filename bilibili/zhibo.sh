#!/bin/bash

#获取直播流地址
roomid="1273106"
live_info=$(curl "http://live.bilibili.com/api/playurl?player=1&cid=${roomid}&quality=0"|grep b1url)
live_url=$(echo $live_info|cut -d '[' -f 3|cut -d ']' -f 1)

#循环推送直播流
while true
do
ps -ef|grep 'ffmpeg'|awk '{print$2}'|xargs kill -9
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




#ffmpeg -i out.mp4 -vf "drawtext=text='lihuibin':fontfile=./fonts/msyh.ttf:fontsize=24:fontcolor=red@0.8:x=w-tw-20:y=h-th-20" -c:v libx264 -c:a copy output8.mp4
#ffmpeg -re -i "$live_url"  -vf "drawtext=text='房间号1273106，主播喵咭喵呜':fontfile=./fonts/msyh.ttf:fontsize=34:fontcolor=yellow@0.8:x=w-text_w:y=text_h"  -vcodec libx264 -acodec copy -b:a 100k -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"

#转码直播
#ffmpeg -i Love.Letter.1995.BluRay.iPad.720p.x264.AAC.3Audio-NYPAD.mp4  -b 200k -s 640x320 out.mp4
#ffmpeg -re -i "./movie/LoveLett.mp4" -vf "drawtext=text='电影名：情书':fontfile=./fonts/msyh.ttf:fontsize=18:fontcolor=white@0.8:x=w-tw-20:y=th" -vcodec libx264 -acodec copy -b:a 128k -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"
