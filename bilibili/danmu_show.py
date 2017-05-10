#!/usr/bin/python
# -*- coding: utf-8 -*-

# gridlayout2.py

import sys
from PyQt5.QtWidgets import * #QWidget, QLabel, QApplication
#from PyQt5.QtWidgets import QWidget, QLabel, QApplication
import time

s='1.Button 按钮。类似标签,但提供额外的功能,例如鼠标掠过、按下、释放以及键盘操作/事件 2.Canvas 画布。\
提供绘图功能(直线、椭圆、多边形、矩形) ;可以包含图形或位图3.Checkbutton 选择按钮。一组方框,可以选择\
其中的任意个(类似 HTML 中的 checkbox)4.Entry 文本框。单行文字域,用来收集键盘输入(类似 HTML 中的 text)5.Frame \
框架。包含其他组件的纯容器6.Label 标签。用来显示文字或图片7.Listbox 列表框。一个选项列表,用户可以从中选择8.Menu\
菜单。点下菜单按钮后弹出的一个选项列表,用户可以从中选择9.Menubutton 菜单按钮。用来包含菜单的组件(有下拉式、层叠式等等)\
10.Message 消息框。类似于标签,但可以显示多行文本11.Radiobutton 单选按钮。一组按钮,其中只有一个可被“按下” (类似 HTML 中的 radio)\
12.Scale 进度条。线性“滑块”组件,可设定起始值和结束值,会显示当前位置的精确值13.Scrollbar 滚动条。对其支持的组件(文本域、画布、列表框、\
文本框)提供滚动功能14.Text 文本域。 多行文字区域,可用来收集(或显示)用户输入的文字(类似 HTML 中的 textarea'

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextBrowser()
        reviewEdit.setText(s+s+s)

        vb=reviewEdit.verticalScrollBar()
        # if vb.value()>=vb.maximum():
        #     return
        # vb.setValue(vb.value() + 2)
        
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        
        self.setLayout(grid)

        self.setWindowTitle('grid layout')
        self.resize(350, 300)

app = QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())
