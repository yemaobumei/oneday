# -*- coding:utf-8 -*-  
import requests
import hashlib
from selenium import webdriver
import time
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
for key in headers:
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
url='http://app0.dreamlive.tv/passport/login/AccountLoginAction.a'


driver = webdriver.PhantomJS() # or add to your PATH	

driver.get(url)

driver.quit()
time.sleep(10)

