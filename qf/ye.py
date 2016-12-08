# -*- coding: utf-8 -*-
import requests,re,time
path=r"./"#数据存放路径




#手机app访问头文件
headers={
'Host': 'client.tyread.com:8080',
'Connection': 'close',
'Accept': '*/*',
#'Connection': 'close',
'NetWorkOperators': 'China Unicom',
'phone-number':'', 
'Client-Agent': 'TYYD_iPhoneOS_10_1_1_OC_4_6_0/750*1334/UnknownDevice',
'NetWorkType': 'WiFi',
'Action': 'getContentInfo',
'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
'guest-id': '1481030839047067',
'APIVersion': '4.0',
'VERSIONCODE': '460',
'User-Agent': 'TYYD/4.6.0 (iPhone; iOS 10.1.1; Scale/2.00)',
'isJailBroke':'0',
'client-imei': '05F7F9F1-4125-4333-8DDC-E693C80D8DA5',
'Adid': '5C8448A1-1D70-4541-A9D3-37187C1382CA',
'qdid': 'AS01',
'Accept-Encoding': 'gzip, deflate'}

cookies={
	'JSESSIONID':'DEB5BCD0BADDE53DD5C9A5E85804F653',
	'pathmodule':'{}',
	'user':"{\"isGuest\":true,\"sessionId\":\"DEB5BCD0BADDE53DD5C9A5E85804F653\",\"userGuestId\":\"1481041410655068\",\"viewType\":1,\"userType\":\"4\"}"
}


 
#每天循环统计数据
def loop(times=30):
	#打开纪录文档
	f_Tuijian=open(path+'TuijianList.txt','wb')
	f_descri=open(path+'description.txt','wb')
	error=open(path+'error.txt','wb')
	#获取主编力荐小说id
	urlTuijianList=r'http://clientwap.tyread.com/androidFive/tuijianList.action?recCtrlId=146645&listName=%E4%B8%BB%E7%BC%96%E5%8A%9B%E8%8D%90&ca=iphone'
	idTuijianList=re.findall('data-bookid=\"(\d+)\"',requests.get(urlTuijianList).content)
	urlBookDetail=r'http://client.tyread.com:8080/portalapi/portalapi?comment=3&contentId=###&mode=1&needMonthInfo=1'
	#纪录榜单小说详细信息
	def top():
		date=time.strftime("%Y-%m-%d ", time.localtime())
		#打开每日推荐榜单纪录文件
		f_day=open(path+date+'Tuijian.txt','wb')
		for id in idTuijianList:
			tempUrl=re.sub('###',id,urlBookDetail)
			regx=r'<contentID>(.*?)</contentID><contentName>(.*?)</contentName><catalogName>(.*?)</catalogName>.*?<authorName>(.*?)</authorName>.*?<description>([\s\S]*?)</description><count>(.*?)</count>'
			#[小说id，小说名，类别，作者，小说简介，阅读量]
			while(True):
				try:
					s=requests.session()
					s.keep_alive=False
					content=s.get(tempUrl,headers=headers).content
					line=re.findall(regx,content)[0]
					t='{0: <40} {1: <20} {2: <20} {3: <10}'.format(line[1],line[2],line[3],line[5])
					f_Tuijian.write(str(t)+'\n')
					f_day.write(str(t)+'\n')
					f_descri.write(line[0]+'  '+line[1]+'\n'+line[-2]+'\n')
					break;
				except IndexError:
					print 'indexerror'
					error.write(content+'\n\n')
				except Exception as e:
					error.write(id+':')
					error.write(str(e.message))
					error.write('\n\n')
					print id,e
				time.sleep(10)				
		f_day.close()

	for i in range(times):
		f_Tuijian.write(time.strftime("%Y-%m-%d ", time.localtime())+'\n')
		f_descri.write(time.strftime("%Y-%m-%d ", time.localtime())+'\n')
		startTime=time.time()
		top()
		endTime=time.time()
		#time.sleep(24*60*60-endTime+startTime)
		#time.sleep(20)	
	f_Tuijian.close()
	f_descri.close()
	error.close()

#高频词汇分析
def word_frequency():
	from collections import Counter
	import jieba
	freqFile=open(r'./freq.txt','wb')
	f_descri=open(path+'description.txt','rb')
	text=f_descri.read()
	words = [word for word in jieba.cut(text, cut_all=False) if len(word) >= 2]
	c = Counter(words)
	for word_freq in c.most_common(15):
		word, freq = word_freq
		print word,freq
		#print isinstance(word,str)		False
		#print isinstance(word,unicode) True
		t='{0:#<20}{1:->10} '.format(word.encode('utf-8'),str(freq))
		freqFile.write(str(t)+'\n')
	freqFile.close()

def popular():
	headers={
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
	'Accept-Encoding': 'gzip, deflate'
	}
	recorder=open(r'./recoder.html','wb')
	url=r'http://wap.tyread.com/pindao/shucheng/paihang/index.html?is_ctwap=0&y=0&id=749&q=1&pageNo=#'
	for i in range(1):
		desUrl=re.sub('#',str(i+1),url)
		regx=r'li[\s\S]*?bookdetail/(\d+?)/gobook'
		response=requests.get(url,headers=headers)
		if response.status_code==200:
			print (re.findall(regx,response.content))
			recorder.write(response.content)
if __name__ == '__main__':
	#loop(1)
	#word_frequency()
	popular()


#主编力鉴：
#http://clientwap.tyread.com/androidFive/tuijianList.action?recCtrlId=146645&listName=%E4%B8%BB%E7%BC%96%E5%8A%9B%E8%8D%90&ca=iphone
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
#获取小说各个标签分类
#Action: getTagsByContentId
#http://client.tyread.com:8080/portalapi/portalapi
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
#获取
#Action: personalizeRecommend
#http://client.tyread.com:8080/portalapi/portalapi?count=9
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
#http://client.tyread.com:8080/portalapi/portalapi?authorId=10050034764220&count=20&start=1
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
#获取小说的id
#Action: getTagsByContentId
#http://client.tyread.com:8080/portalapi/portalapi?contentId=10000002266925267
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
#获取小说详细信息，如作者姓名，阅读量，简介
#'Action': 'getContentInfo'
#http://client.tyread.com:8080/portalapi/portalapi?comment=3&contentId=10000002266925267&mode=1&needMonthInfo=1
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
#获取小说内容
#http://client.tyread.com:8080/portalapi/portalapi?contentId=10000002266925267&count=9&start=1
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
#wap版本小说详细信息
#url=r"http://wap.tyread.com/bookdetail/10000002266925267/gobookinfo.html?is_ctwap=0&bookId=10000002287685376&fromModule=J-index-zbRec-content-1"
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

#作者id:authorID
#作者姓名：authorName
#小说id：contentID
#小说读量：count
#小说简介：description


