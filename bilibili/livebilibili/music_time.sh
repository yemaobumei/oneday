ffmpeg -f avfoundation -i "1:0"  -c:v libx264 -c:a aac  -strict experimental -b:a 192k  -shortest -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075"                         

ffmpeg -f avfoundation -i "1:0" -vcodec libx264  -acodec aac -b:a 192k -ac 1 -shortest  -f flv "rtmp://xl.live-send.acg.tv/live-xl/?streamname=live_25303175_5745325&key=71771fb7bb37ccbdc17888f178f56075" 
