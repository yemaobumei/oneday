# -*- coding:utf-8 -*-  
import requests
import hashlib,time

# md5 = hashlib.md5()
# md5.update('ye06021123')
# print md5.hexdigest()
#>>>9ef1969d6ed8fc9a289ef6b0e48e13b6
headers={
	'Host': 'app0.dreamlive.tv',
	'Accept': '*/*',
	'Connection': 'keep-alive',
	'app_ct': 'CN',
	'app_v': '2.0.9',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Content-Length': '163',
	'User-Agent': 'Dreamer/2.0.9 (iPhone; iOS 10.1.1; Scale/2.00)',
	'Connection': 'keep-alive',
	'app_type': '0',
	'Cookie': 'JSESSIONID=F9F975F8153A46BEAC2BB0F70CAE3B0E',
	'app_dev': '5C8448A1-1D70-4541-A9D3-37187C1382CA'
}
t=str(int(time.time()))
md5 = hashlib.md5()
md5.update(t)
m_check=md5.hexdigest()
print m_check
data='account=13126772351&deviceId=5C8448A1-1D70-4541-A9D3-37187C1382CA&mcheck='+m_check+'&password=9ef1969d6ed8fc9a289ef6b0e48e13b6&r='+str(int(time.time()))
# params={
# 	'account':'13126772351',
# 	'deviceId':'5C8448A1-1D70-4541-A9D3-37187C1382CA',
# 	'mcheck':'4bd4b051e5e83707ec2a4914473efeff',
# 	'password':'9ef1969d6ed8fc9a289ef6b0e48e13b6',
# 	'r':'1484561989673'
# }
# cookies={'JSESSIONID':'58E63DB365210FD77B1C1BC2E2CD3F5B'}
url='http://app0.dreamlive.tv/passport/login/AccountLoginAction.a'
requests.post(url,headers=headers,data=data)



