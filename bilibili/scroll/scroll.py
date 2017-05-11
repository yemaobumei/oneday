
from PyQt4 import  QtGui, QtCore 

from PyQt4.QtCore import Qt
import time
import sys
import json
import asyncio
from tuodong import ShadowWidget
class Text(QtGui.QTextBrowser):
	 
	def __init__(self, parent=None):
		super(Text, self).__init__(parent)
		#self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
		self.initUI()
		 
			 
	def initUI(self):

		self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow )
		#self.set_transparency(True)
		self.setStyleSheet("background: rgba(14,27,44,60%);color:yellow;font-size:15px;font-weight:bold;font-family:Helvetica")


	# def checkButton(self,data):
	# 	self.moveCursor(QtGui.QTextCursor.End)
	# 	#self.showLogText.append(self.IPHostnameEdit.text())		
	# 	self.append(data)

	def set_transparency(self, enabled):
		if enabled:
			self.setAutoFillBackground(False)
		else:
			self.setAttribute(Qt.WA_NoSystemBackground, False)

		self.setAttribute(Qt.WA_TranslucentBackground, enabled)
		self.repaint() 
	
  

class Windows(ShadowWidget):
	def __init__(self):
		super(Windows, self).__init__()
		self.initUI()
		self.setWindowTitle('弹幕姬测试')
		self.setFixedSize(380,380)
		
	


		self.label = QtGui.QLabel('观众：')      
		self.label2 = QtGui.QLabel('其他待定')


		# Message / Log
		self.text=Text()
		self.text.setText("{0} initializing...".format(time.strftime("%F %T")))

		# layout for IPHostname
		self.StatusLayout = QtGui.QHBoxLayout()
		self.StatusLayout.addWidget(self.label)
		self.StatusLayout.addWidget(self.label2)

		# layout 
		self.mainLayout = QtGui.QVBoxLayout()
		self.mainLayout.addLayout(self.StatusLayout)
		self.mainLayout.addWidget(self.text)	
		self.setLayout(self.mainLayout)
		

 

	def initUI(self):

		#self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow )
		self.set_transparency(True)
		self.setStyleSheet("background: rgba(14,27,44,60%);color:yellow;font-size:15px;font-weight:bold;font-family:Helvetica")

	def checkButton(self,data):
		#self.moveCursor(QtGui.QTextCursor.End)
		#self.showLogText.append(self.IPHostnameEdit.text())
		data=json.loads(data)
		#self.text.append(data['commentUser'])		
		self.text.append(str(data['level'])+data['commentUser']+data['commentText']) 
		# data={
		# 		'isAdmin':isAdmin,'isVIP':isVIP,'level':level,'xun_level':xun_level,'xun_name':xun_name,
		# 		'commentUser':commentUser,'commentText':commentText,'cmd':cmd
		# 	}

	def changeInfo(self,info):
		self.label.setText('观众:'+info)
	def set_transparency(self, enabled):
		if enabled:
			self.setAutoFillBackground(False)
		else:
			self.setAttribute(Qt.WA_NoSystemBackground, False)

		self.setAttribute(Qt.WA_TranslucentBackground, enabled)
		#self.setWindowOpacity(0)
		self.repaint() 

 
	  
# app = QtGui.QApplication(sys.argv)
# win = Text()
# win.show()
# app.exec_()
