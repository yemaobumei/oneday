import requests,urllib
headers={
'Host': 'app0.dreamlive.tv:7777',
'Content-Type': 'application/x-www-form-urlencoded',
'Connection': 'keep-alive',
'Accept': '*/*',
'User-Agent': 'Dreamer/2.0.9 (iPhone; iOS 10.1.1; Scale/2.00)',
'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
'Content-Length': '259',
'Accept-Encoding': 'gzip, deflate',
'Cookie': 'JSESSIONID=E9FA852704B277FFD55FF1645ADAAA4D',
'app_dev': '5C8448A1-1D70-4541-A9D3-37187C1382CA',
}
cookies={'JSESSIONID':'58E63DB365210FD77B1C1BC2E2CD3F5B'}
data='anchor_id=10062712&chat_message=%E5%96%9C%E6%AC%A2&chat_time=1482501220534&deviceId=9E315CA5-0E91-4A94-823B-32D9BA997B4D&mcheck=c5147158c1ed35a46c2ea99d52a9e373&r=1482501220537&room_id=5898635&user_id=10419145&user_token=token_1788c0006845a1ea8666a8a8e3e43ddc'

url='http://app.dreamlive.tv:7777//chatrecord?'
for i in range(100):
    s=requests.post(url,headers=headers,data=data)
    print s.status_code

