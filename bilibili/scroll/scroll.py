
from PyQt4 import  QtGui, QtCore 

from PyQt4.QtCore import Qt
import time
import sys

import asyncio
from tuodong import ShadowWidget
# class Text(QtGui.QTextBrowser):
     
#     def __init__(self, parent=None):
#         super(Text, self).__init__(parent)
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
         
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
#             QApplication.postEvent(self, QEvent(174))
#             event.accept()
 
#     def mouseMoveEvent(self, event):
#         if event.buttons() == Qt.LeftButton:
#             self.move(event.globalPos() - self.dragPosition)
#             event.accept()
             

	
  

class Windows(ShadowWidget):
	def __init__(self):
		super(Windows, self).__init__()
		self.initUI()
		self.setWindowTitle('PyQt4 QTextEdit')
		self.setFixedSize(380,380)
		
	
		
		# Message / Log
		self.showLogText = QtGui.QTextBrowser()#QTextEdit()#QTextBrowser()

		self.showLogText.setText("{0} initializing...".format(time.strftime("%F %T")))
		self.showLogText.setStyleSheet("background: rgba(14,27,44,60%);color:yellow;font-size:15px;font-weight:bold;font-family:Helvetica")

		
		# layout 
		self.mainLayout = QtGui.QVBoxLayout()
		self.mainLayout.addWidget(self.showLogText)	
		self.setLayout(self.mainLayout)
		

 

	def initUI(self):

		self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow )

		self.set_transparency(True)


	def checkButton(self,data):
		self.showLogText.moveCursor(QtGui.QTextCursor.End)
		#self.showLogText.append(self.IPHostnameEdit.text())		
		self.showLogText.append(data)

	def set_transparency(self, enabled):
		if enabled:
			self.setAutoFillBackground(False)
		else:
			self.setAttribute(Qt.WA_NoSystemBackground, False)
		#下面这种方式好像不行
		# pal=QtGui.QPalette()
		# pal.setColor(QtGui.QPalette.Background, QColor(127, 127,10,120))
		# self.setPalette(pal) 
		self.setAttribute(Qt.WA_TranslucentBackground, enabled)

		#self.setWindowOpacity(0)
		self.repaint() 

 
	  
# app = QtGui.QApplication(sys.argv)
# win = Text()
# win.show()
# app.exec_()
