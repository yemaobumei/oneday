# -*- coding: utf-8 -*-
import chardet,codecs
path='./'
fi=open(path+'TuijianList.txt','rb')
fo=open(path+'TuijianList_gbk.txt','wb')
data=fi.read()
if data[:3] == codecs.BOM_UTF8:
    data = data[3:]
print chardet.detect(data)

c=data.decode('utf-8').encode('gbk')
fo.write(c)

#fo.write(c.encode('gbk'))
fi.close()
fo.close()
fs=open(path+'test.txt','wb')
c=u'喜欢'
c=c.encode('gbk')

fs.write(c)
fs.close()
