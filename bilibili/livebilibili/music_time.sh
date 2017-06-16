#!/bin/bash

function rand(){  
    min=$1  
    max=$(($2-$min+1))  
    num=$(($RANDOM+1000000000)) #增加一个10位的数再求余  
    echo $(($num%$max+$min))  
} 

font_path="/usr/share/fonts/winFonts/msyh.ttf"
	rnd=$(rand 1 2) 
	ffmpeg  -loop 1 -i "0${rnd}.jpg"   -pix_fmt yuv420p -vcodec libx264 -b:v 100k  -preset medium -crf 18  -vframes 250 -r 10 -t 10 -s 960x540 -y SinglePictureVide.mp4
while true
do
if [ "$(ls|grep .mp3)" != "" ]
then
	for file in $(ls -rt *.mp3| tr " " "\?")
	do
		rest=$(ls |grep '.mp3'|wc -l)
		echo $rest
		ffmpeg -re  -i SinglePictureVide.mp4 -i "${file}" -vf "drawtext=text='点歌：点歌+歌名 切歌：切歌 切歌可能需要手动刷新直播间页面 ':fontfile=${font_path}:fontsize=18:fontcolor=yellow@0.8:x=w-tw-10:y=th,drawtext=text='正在播放：${file}   当前歌单还有${rest}首':fontfile=${font_path}:fontsize=18:fontcolor=yellow@0.8:x=w-tw-30:y=2*th+10" -c:v libx264 -b:v 600k -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"
		rm "${file}"
	done 
else
	f=$(ls bgm/*.mp3 | sort -R | head -n1)
	ffmpeg -re  -i SinglePictureVide.mp4 -i	"${f}" -vf "drawtext=text='点歌：点歌+歌名 切歌：切歌 切歌可能需要手动刷新直播间页面 ':fontfile=${font_path}:fontsize=18:fontcolor=yellow@0.8:x=w-tw-10:y=th,drawtext=text='正在播放${f}   当前无人点歌':fontfile=${font_path}:fontsize=18:fontcolor=yellow@0.8:x=w-tw-30:y=2*th+10" -c:v libx264 -b:v 600k -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"

fi
done


ffmpeg -loop 1 -re -i "0${rnd}.jpg" -i 1.mp3 -i "${file}" -vf "drawtext=text='点歌：点歌+歌名 切歌：切歌 切歌可能需要手动刷新直播间页面 ':fontfile=${font_path}:fontsize=18:fontcolor=yellow@0.8:x=w-tw-10:y=th,drawtext=text='正在播放：${file}   当前歌单还有${rest}首':fontfile=${font_path}:fontsize=18:fontcolor=yellow@0.8:x=w-tw-30:y=2*th+10" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"

