# -*- coding:utf-8 -*-
import PIL
from PIL import Image
import pytesseract

#1. 打开图片
im=Image.open(r'C:\Users\Administrator\bilibili\cap.png')

#2. 将彩色图像转化为灰度图
im = im.convert('L')

#3. 降噪，图片二值化
def initTable(threshold=50):
	table = []
	for i in range(256):
		if i < threshold:
			table.append(0)
		else:
			table.append(1)

	return table

binaryImage = im.point(initTable(), '1')
binaryImage.show()
text=pytesseract.image_to_string(binaryImage, config='-psm 7')
print text,222
