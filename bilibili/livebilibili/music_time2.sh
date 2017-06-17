# !/bin/bash

function rand(){  
    min=$1  
    max=$(($2-$min+1))  
    num=$(($RANDOM+1000000000)) #增加一个10位的数再求余  
    echo $(($num%$max+$min))  
} 

font_path="/usr/share/fonts/winFonts/msyh.ttf"
fontcolor="yellow"
fontsize="24"

#rnd=4 
declare -i rest
	#ffmpeg  -loop 1 -i "0${rnd}.jpg"   -pix_fmt yuv420p -vcodec libx264 -b:v 100k -r:v 25 -preset medium -crf 18  -vframes 250  -t 10 -s 960x540 -y SinglePictureVide.mp4
while true
do
#rnd=$(rand 1 15)
pic=$(ls *.jpg | sort -R | head -n1)
if [ "$(ls|grep .mp3)" != "" ]
then
	for file in $(ls -rt *.mp3| tr " " "\?")
	do
		rest=$(ls |grep '.mp3'|wc -l)-1
		echo $rest
		drawtext1="drawtext=text='点歌：点歌+歌名歌手 切歌：切歌  点歌机在网易云搜索并下载 ':fontfile=${font_path}:fontsize=${fontsize}:fontcolor=${fontcolor}@0.8:x=w-tw-30:y=10,drawtext=text='正在播放：${file}   点播列表还有${rest}首':fontfile=${font_path}:fontsize=${fontsize}:fontcolor=${fontcolor}@0.8:x=w-tw-30:y=th+20,drawtext=text='爱特夜猫，调戏弹幕姬':fontfile=${font_path}:fontsize=${fontsize}:fontcolor=white@0.8:x=w-tw-30:y=2*(th+10)+10"
		ffmpeg -loop 1 -re -i "${pic}"  -i "${file}" -vf  "${drawtext1}" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"


#		ffmpeg   -i SinglePictureVide.mp4 -i "${file}" -vf "drawtext=text='点歌：点歌+歌名 切歌：切歌 切歌可能需要手动刷新直播间页面 ':fontfile=${font_path}:fontsize=18:fontcolor=yellow@0.8:x=w-tw-10:y=th,drawtext=text='正在播放：${file}   当前歌单还有${rest}首':fontfile=${font_path}:fontsize=18:fontcolor=yellow@0.8:x=w-tw-30:y=2*th+10"  -b:v 400k -b:a 256k -f flv -y "upload.flv"

#		ffmpeg -re  -i upload.flv -c copy -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"
		rm "${file}"
	done 
else
	
	file=$(ls bgm/*.mp3 | sort -R | head -n1)
	#ffmpeg -re   -i	"${f}" -c copy -b:v 200k -b:a 192k  -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"
	drawtext2="drawtext=text='点歌：点歌+歌名歌手 切歌：切歌  点歌机在网易云搜索并下载 ':fontfile=${font_path}:fontsize=${fontsize}:fontcolor=${fontcolor}@0.8:x=w-tw-30:y=10,drawtext=text='正在播放：${file}   当前无人点歌':fontfile=${font_path}:fontsize=${fontsize}:fontcolor=${fontcolor}@0.8:x=w-tw-30:y=th+20,drawtext=text='爱特夜猫，调戏弹幕姬':fontfile=${font_path}:fontsize=${fontsize}:fontcolor=white@0.8:x=w-tw-30:y=2*(th+10)+10"
	echo $drawtext2
	ffmpeg -loop 1 -re -i "${pic}"  -i "${file}"  -vf "${drawtext2}"  -strict experimental -c:v libx264 -c:a aac -b:a 192k   -shortest  -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"

fi	
done
