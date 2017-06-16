#!/bin/bash

function rand(){  
    min=$1  
    max=$(($2-$min+1))  
    num=$(($RANDOM+1000000000)) #增加一个10位的数再求余  
    echo $(($num%$max+$min))  
} 

font_path="/usr/share/fonts/winFonts/msyh.ttf"
rnd=$(rand 0 6)

ffmpeg  -loop 1 -i "0${rnd}.jpg"   -pix_fmt yuv420p -vcodec libx264 -b:v 600k -r:v 25 -preset medium -crf 30  -vframes 250 -r 25 -t 10 -s 720x576 -y SinglePictureVide.mp4

declare -i x=0


if [ "$(ls *.mp3)" != '' ]; then 
	rm *.mp3
fi

if [ "$(ls *.txt)" != '' ]; then 
        rm *.txt
fi

while true
do
playlist="list${x}.txt"
if [ -f "$playlist" ]; 
then
	songName=$(cat ${playlist})	
	netease-dl --quiet song --name  $songName
	file=$(ls *.mp3)
	if [ "$file" != '' ]; then
		#seconds=$(python3 -c "import eyed3;s=eyed3.load('${file}');print(s.info.time_secs)")
	
		#ffmpeg  -loop 1 -i "0${rnd}.jpg"   -pix_fmt yuv420p -vcodec libx264 -b:v 500k -r:v 25 -preset medium -crf 30  -vframes 250 -r 25 -t ${seconds} -s 720x576 -y SinglePictureVide.mp4

		ffmpeg -re -i SinglePictureVide.mp4 -i "${file}" -vf "drawtext=text='点歌格式：点歌+歌曲名 正在播放：$file':fontfile=${font_path}:fontsize=18:fontcolor=yellow@0.8:x=w-tw-10:y=th" -c:v libx264 -b:v 500k -b:a 256k -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"

		rm *.mp3
	else
		echo "没有找到歌曲:${songName}"
	fi
	x=x+1
else
	echo "无人点歌"
	sleep 3
fi

done
