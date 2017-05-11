# coding:utf-8  
from PyQt4.Qt import *  
import sys  
  
PADDING=4   
sys.setrecursionlimit(10000)  
class ShadowWidget(QWidget):  
    def __init__(self, parent=None):
        super(ShadowWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow )
         
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()
 
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
             