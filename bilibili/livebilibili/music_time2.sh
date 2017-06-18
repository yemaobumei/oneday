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
LIVEURL="rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"
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
		drawtext1="drawtext=text='点歌：点歌+歌名歌手 切歌：切歌  点歌机在网易云搜索并下载 ':fontfile=${font_path}:fontsize=0.03*main_h:fontcolor=${fontcolor}@0.8:x=w-tw-30:y=10,drawtext=text='正在播放：${file}   点播列表还有${rest}首':fontfile=${font_path}:fontsize=0.03*main_h:fontcolor=${fontcolor}@0.8:x=w-tw-30:y=th+20,drawtext=text='爱特夜猫，调戏弹幕姬':fontfile=${font_path}:fontsize=0.03*main_h:fontcolor=white@0.8:x=w-tw-30:y=2*(th+10)+10"
		# ffmpeg -loop 1 -re -i "${pic}"  -i "${file}" -vf  "${drawtext1}" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv "${LIVEURL}"
		lrc="$(echo $file|cut -d "." -f 1).lrc"
		if test -f "lyric/$lrc" && cat "lyric/$lrc" | grep -v "not found" 
		then
			subtitles="subtitles=f=lyric/${lrc}:force_style='FontName=Arial,FontSize=14'"
			ffmpeg -loop 1 -re -i "${pic}"  -i "${file}" -vf  "${drawtext1},${subtitles}" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv "${LIVEURL}"		
		else			
			ffmpeg -loop 1 -re -i "${pic}"  -i "${file}" -vf  "${drawtext1}" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv "${LIVEURL}"
		fi		
		rm "${file}"
	done 
else
	
	file=$(ls bgm/ | sort -R | head -n1) ##file=$(ls bgm/* | sort -R | head -n1)输出包含bgm/,ls bmg/ 不包含
	#ffmpeg -re   -i	"${f}" -c copy -b:v 200k -b:a 192k  -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"
	drawtext2="drawtext=text='点歌：点歌+歌名歌手 切歌：切歌  点歌机在网易云搜索并下载 ':fontfile=${font_path}:fontsize=0.03*main_h:fontcolor=${fontcolor}@0.8:x=w-tw-30:y=10,drawtext=text='正在播放：${file}   当前无人点歌':fontfile=${font_path}:fontsize=0.03*main_h:fontcolor=${fontcolor}@0.8:x=w-tw-30:y=th+20,drawtext=text='爱特夜猫，调戏弹幕姬':fontfile=${font_path}:fontsize=0.03*main_h:fontcolor=white@0.8:x=w-tw-30:y=2*(th+10)+10"
	
	if [ "$(echo ${file}|grep .mp3)" != "" ]
	then
		lrc="$(echo $file|cut -d "." -f 1).lrc"
		if test -f "bgm/lyric/$lrc" && cat "bgm/lyric/$lrc" | grep -v "not found" 
		then
			subtitles="subtitles=f=bgm/lyric/${lrc}:force_style='FontName=Arial,FontSize=14'"
			ffmpeg -loop 1 -re -i "${pic}"  -i "bgm/${file}" -vf  "${drawtext2},${subtitles}" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv "${LIVEURL}"		
		else			
			ffmpeg -loop 1 -re -i "${pic}"  -i "bgm/${file}" -vf  "${drawtext2}" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv "${LIVEURL}"
		fi			
		# ffmpeg -loop 1 -re -i "${pic}"  -i "bgm/${file}"  -vf "${drawtext2}"  -strict experimental -c:v libx264 -c:a aac -b:a 192k   -shortest  -f flv "${LIVEURL}"
	else
		ffmpeg -re -i "bgm/${file}" -vf "${drawtext2}" -vcodec libx264  -b:v 600k  -f flv "${LIVEURL}"
	fi
fi	
done

#  ffmpeg -loop 1 -y -i 01.jpg  -i 1.mp3 -vf subtitles="f=input.srt:force_style='FontName=Arial,FontSize=14'" -shortest test1.mp4


# lrc="$(echo $file|cut -d "." -f 1).lrc"
# if [[ $(cat "lyric/$lrc") =~ "not found" ]]
# then
# 	ffmpeg -loop 1 -re -i "${pic}"  -i "${file}" -vf  "${drawtext1}" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv "${LIVEURL}"
# else
# 	subtitles="subtitles=f=lyric/${lrc}:force_style='FontName=Arial,FontSize=14'"
# 	ffmpeg -loop 1 -re -i "${pic}"  -i "${file}" -vf  "${drawtext1},${subtitles}" -c:v libx264 -c:a aac  -strict experimental -b:a 192k -shortest  -f flv "${LIVEURL}"
# fi

