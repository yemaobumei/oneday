#! /usr/bin/env python  
# -*- coding: utf-8 -*-  
  
from PyQt4 import QtCore, QtGui  
import time  
import txt  
  
  
class MyWidget(QtGui.QWidget):  
    def __init__(self, parent=None):  
        super(MyWidget, self).__init__(parent)  
  
        #self.resize(800, 500)  
        self.setWindowTitle('实时显示热门微博内容')  
  
        self.timer = QtCore.QTimer()  
        #显示微博内容  
        self.txt = QtGui.QTextBrowser() #QTextEdit()  
        #显示微博关键字  
        self.txt_key = QtGui.QLineEdit()  
        #显示微博用户  
        self.txt_name = QtGui.QLineEdit()  
  
        label1 = QtGui.QLabel("微博用户名:")  
        label2 = QtGui.QLabel("关键字：")  
        label3 = QtGui.QLabel("微博内容:")  
        otherLabel = QtGui.QLabel("备注:")  
        otherLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)  
  
        labelCol = 0  
        contentCol = 1  
  
        leftLayout = QtGui.QGridLayout()  
        leftLayout.addWidget(label1, 0, labelCol)  
        leftLayout.addWidget(self.txt_name, 0, contentCol, 1, 40)  
        leftLayout.addWidget(label2, 1, labelCol)  
        leftLayout.addWidget(self.txt_key, 1, contentCol, 1, 40)  
        leftLayout.addWidget(label3, 2, labelCol)  
        leftLayout.addWidget(self.txt, 2, contentCol, 1, 40)  
        leftLayout.addWidget(otherLabel, 5, labelCol, 1, 40)  
        leftLayout.setColumnStretch(0, 1)  
        leftLayout.setColumnStretch(1, 3)  
  
        self.ok_button = QtGui.QPushButton("开始爬虫", self)  
        self.closePushButton = QtGui.QPushButton("关闭", self)  
  
        rightLayout = QtGui.QVBoxLayout()  
        rightLayout.setMargin(10)  
        rightLayout.addStretch(7)  
        rightLayout.addWidget(self.ok_button)  
        rightLayout.addWidget(self.closePushButton)  
  
        mainLayout = QtGui.QGridLayout(self)  
        mainLayout.setMargin(15)  
        mainLayout.setSpacing(15)  
        mainLayout.addLayout(leftLayout, 0, 0)  
        mainLayout.addLayout(rightLayout, 0, 1)  
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)  
  
        self.connect(self.ok_button, QtCore.SIGNAL('clicked()'),self, QtCore.SLOT("on_ok_button_clicked()"))  
        self.connect(self.closePushButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))  
  
  
    # 自定义实现爬虫的槽函数  
    @QtCore.pyqtSlot()  
    def on_ok_button_clicked(self):  
        self.txt.clear()  
        for i in range(len(txt.txt)):  
            #进行添加内容  
            self.txt_name.setText(txt.txt_name[i])  
            self.txt.setText('  '+txt.txt[i])  
            self.txt_key.setText(txt.txt_key[i])  
            # 下面两条语句用于设置单条微博显示时间  
            QtGui.QApplication.processEvents()  
            time.sleep(2)  
            self.txt.clear()  
  
if __name__ == "__main__":  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    app.aboutToQuit.connect(app.deleteLater)  
    w = MyWidget()  
    w.show()  
    app.exec_()  
