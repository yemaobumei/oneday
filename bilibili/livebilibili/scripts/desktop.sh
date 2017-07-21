#!/bin/bash
#ffmpeg -f avfoundation -i "1:0"  -c:v libx264 -c:a aac  -strict experimental -b:a 192k  -shortest -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"                         
#ffmpeg -f avfoundation -i "1:0" -vcodec libx264  -acodec aac -b:a 192k -ac 1 -shortest  -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075" 

rtmp="rtmp://txy.live-send.acg.tv/live-txy/?streamname=live_107855207_5704224&key=40ba86aa0095132e3fdcb9174c56ef0a"

ffmpeg -f avfoundation -i "1:0" -vcodec libx264  -acodec aac -b:a 192k -ac 1 -shortest  -f flv "${rtmp}"