#!/usr/bin/env python

#encoding=utf-8

"""

著作权归作者所有。

商业转载请联系作者获得授权，非商业转载请注明出处。

作者：yf

链接：http://www.zhihu.com/question/20399991/answer/62551736

来源：知乎

"""





import re, requests
import re, requests



SAVE_DIR_PATH = r'c:\pic\ '

URL = 'http://www.zhihu.com/question/37006507'

save = lambda url: open(SAVE_DIR_PATH+url[url.rfind('/')+1:], 'wb').write(requests.get(url).content)



if __name__ == '__main__':

    map(save, [url[1] for url in re.findall(ur'(<img.*?src=["])(https://pic.+?)(["].+?jpg">)', requests.get(URL).content)])

    open(r'c:\python27\oneday_one\list.txt','w').write(requests.get(URL).content)`
