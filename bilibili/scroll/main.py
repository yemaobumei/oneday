import asyncio
import sys
from bilibiliClient import bilibiliClient

from scroll import Windows
from PyQt4 import  QtGui

from quamash import QEventLoop, QThreadExecutor

danmuji = bilibiliClient()

app = QtGui.QApplication(sys.argv)

loop = QEventLoop(app)
asyncio.set_event_loop(loop)




tasks = [
			danmuji.connectServer() ,
			danmuji.HeartbeatLoop()
		]


with loop: ## context manager calls .close() when loop completes, and releases all resources

    win = Windows()
    danmuji.update_data.connect(win.checkButton)
    danmuji.update_info.connect(win.changeInfo)
    win.show()
    loop.run_until_complete(asyncio.wait(tasks))





