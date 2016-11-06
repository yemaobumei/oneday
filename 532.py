#!/usr/bin/env python
#encoding=utf-8
import urllib,os,re,datetime

#视频播放地址
url=r'http://532movie.bnu.edu.cn/player/2560-4.html'

#下载视频存放位置
path=r'c:\\'

#获取视频下载地址前缀
def get_url(video_url):
    #正则表达式匹配地址
    reg2="uploads/video.*?wl"
    reg1="http://172.16.215.*?/"
    reg3=u'正在播放'
    html=urllib.urlopen(video_url).read()
    try:
        URL=re.findall(reg1,html)[0]+re.findall(reg2,html)[0]+'_'
    except Exception,e:
        print '该视频地址不存在'
        return None
    print '视频下载地址前缀: '+URL
    return URL

#获取视频片段地址的后缀
def f(number):
    string=str(number)
    temp=''
    for i in range(7-len(string)):
        temp+='0'
    url_suffix=temp+string+r'.ts'
    return url_suffix #0000001.ts

#下载视频,合并视频
def download(url_prefix):
    if not url_prefix:
        return 
    i=1
    video=open(path+r'target.mp4','wb')        
    while(True):
        #完整视频片段下载地址
        URL=url_prefix+f(i)
        print '正在下载片段： '+str(i)
        #存储视频片段的完整路径名
        file_name=path+str(i)+r'.ts'
        i+=1
        #判断视频片段遍历是否到头
        try:
            state=urllib.urlopen(URL).getcode()
            if(state==404):
                break
        except Exception, e:
            print '发生错误: '+e
            break
        #下载视频片段
        urllib.urlretrieve(URL,file_name)

        #合并视频
        file_=open(file_name,'rb')
        video.write(file_.read())
        file_.close()
        #删除视频片段
        os.remove(file_name)      
    video.close()
    print 'finished'
    



if __name__ == '__main__':
    starttime=datetime.datetime.now()
    URL=get_url(url)
    download(URL)
    endtime=datetime.datetime.now()
    print 'use'+str((endtime-starttime).seconds/60.0)+'minutes'
