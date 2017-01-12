from selenium import webdriver
import time
headers={
'Host': 'h5.weiyingonline.com',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'Cookie': 'totoro_cookie=1484129147647_9300; totoro_share_click_cookie=1484129147638_1808; JSESSIONID=685BEB546B16CF9F86BA068B39BBA22D',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Mobile/14B100 MicroMessenger/6.5.3 NetType/WIFI Language/zh_CN',
'Accept-Language': 'zh-cn',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive'
}
for key in headers:
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
url='http://h5.weiyingonline.com/share_play/SharePlayClickAction.a?shareDetailId=1190267'

for i in range(3):
    driver = webdriver.PhantomJS() # or add to your PATH	
    print i
    driver.get(url)
    time.sleep(1)
#    driver.quit()
time.sleep(10)

