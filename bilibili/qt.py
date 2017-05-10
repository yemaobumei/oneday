import sys
from PyQt4 import QtGui, QtCore

class mymainwindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)

app = QtGui.QApplication(sys.argv)
mywindow = mymainwindow()
mywindow.show()
app.exec_()
mywindow.show()