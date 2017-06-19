#/bin/bash

#一些公用参数设定
font_path="Arial.ttf"
fontcolor="yellow"
fontsize="24"
LIVEURL="rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"

file="$(ls *mp3)"
pic="7.jpg"
drawtext2="drawtext=text='Linux系统下FFMPEG推流加py弹幕姬实现弹幕点歌':fontfile=${font_path}:fontsize=${fontsize}:fontcolor=${fontcolor}@0.8:x=w-tw-30:y=th+20"

echo $drawtext2  

ffmpeg -loop 1 -re -i "${pic}"  -i "${file}" -vf "${drawtext2}" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv -y out.flv		

