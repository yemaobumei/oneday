#!/bin/bash
while true
do
result=$(curl 'http://live.bilibili.com/api/playurl?player=1&cid=1273106&quality=0 '|grep b1url)
if [[ $result =~ 'CDATA' ]]
then
  live_url=$(curl 'http://live.bilibili.com/api/playurl?player=1&cid=1273106&quality=0 '|grep b1url|cut -d '[' -f 3|cut -d ']' -f 1) 
  ffmpeg -re -i "$live_url" -vcodec copy -acodec aac -b:a 100k -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"  
else
  ffmpeg -re -i "miao4_2_x264.mp4" -vcodec copy -acodec aac -b:a 192k -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"
fi
done
