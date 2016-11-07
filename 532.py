#encoding=utf-8
import urllib,os,re,datetime

#视频播放地址
url=r'http://532movie.bnu.edu.cn/movie/2594.html'
#下载从第几集开始到第几集结束
start=1
end=4
#下载视频存放位置
path=r'c:\\'

#获取视频下载地址前缀
def get_url(video_url):
    #正则表达式匹配地址
    reg2="uploads/video.*?wl"
    reg1="http://172.16.215.*?/"
    temp=urllib.urlopen(video_url)    
    html=temp.read()   
    try:
        prefix=re.findall(reg1,html)[0]
        URL=re.findall(reg2,html)
        for j in range(len(URL)):
            URL[j]=prefix+URL[j]+'_'
    except Exception,e:
        print '该视频地址不存在aa'
        return None
    temp.close()    
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
def download(url_prefix,filename,index):
    if not url_prefix:
        return 
    i=1
    print '目标位置: ',filename     
    video=open(filename,'wb')        
    while(True):
        #完整视频片段下载地址
        URL=url_prefix+f(i)
        print '正在下载第%s集片段%s '%(index,i)
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
        #urllib.urlretrieve(URL,file_name) #直接将视频片段下载到本地
        
        #合并视频
        file_=urllib.urlopen(URL)#打开远程视频，像本地文件一样操作这个文件对象来获取远程数据，
        video.write(file_.read())
        file_.close()
        #删除视频片段
        #os.remove(file_name)      
    video.close()
#启动程序
def main():
    i=start  
    reg=ur'title.*?([/\s0-9a-zA-Z\u4e00-\u9fa5]+).*?'
    html=urllib.urlopen(url).read()
    to_dir=re.findall(reg,html.decode('utf-8'))[0]+r'\\'
    to_dir=path+re.sub('[\s/]+','-',to_dir)
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    video_url=url
    video_url=video_url.replace('.html','-'+str(1)+'.html').replace('/movie','/player')
    #print video_url
    URL=get_url(video_url)
    #print URL
    while (i<=end and i<=len(URL)):
        print '第%s集开始下载'%(i)
        filename=to_dir+str(i)+'.mp4'
        download(URL[i-1],filename,i) 
        i+=1
    print 'finished'   
    return None

if __name__ == '__main__':
    starttime=datetime.datetime.now()
    main()
    endtime=datetime.datetime.now()
    print 'use: '+str((endtime-starttime).seconds/60.0)+' minutes'
