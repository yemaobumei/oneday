#!/usr/bin/env python3 
# Author：1626478661
# Date：2016-09-06 15:28:21
# PyQt5 QTextEdit 
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
import sys
import time
class Windows(QWidget):
    def __init__(self):
        super(Windows, self).__init__()
        
        self.setWindowTitle('PyQt5 QTextEdit © QQ 1626478661')
        self.setFixedSize(300, 150)
        
        # IP address / Hostname
        self.IPHostnameEdit = QLineEdit()
        self.IPHostnameEdit.setPlaceholderText('IP address or Hostname')
        self.IPHostnameButton = QPushButton('追加')
        self.IPHostnameButton.clicked.connect(self.checkButton)
        
        self.IPHostnameButton02 = QPushButton('分行')
        self.IPHostnameButton02.clicked.connect(self.checkButton02)
        
        # Message / Log
        self.showLogText = QTextEdit()
        self.showLogText.setText("{0} initializing...".format(time.strftime("%F %T")))
        
        
        # layout for IPHostname
        self.IPHostnameLayout = QHBoxLayout()
        self.IPHostnameLayout.addWidget(self.IPHostnameEdit)
        self.IPHostnameLayout.addWidget(self.IPHostnameButton)
        self.IPHostnameLayout.addWidget(self.IPHostnameButton02)
        
        # layout 
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.IPHostnameLayout)
        self.mainLayout.addWidget(self.showLogText)
        
        self.setLayout(self.mainLayout)
        
        # Disable zoom- / zoom+
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        
    # Function for check Button 
    def checkButton(self):
        self.showLogText.moveCursor(QTextCursor.End)
        self.showLogText.insertPlainText(self.IPHostnameEdit.text())
        
    def checkButton02(self):
        self.showLogText.moveCursor(QTextCursor.End)
        self.showLogText.append(self.IPHostnameEdit.text())
        
        
app = QApplication(sys.argv)
win = Windows()
win.show()
app.exec_()