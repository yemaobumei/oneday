import asyncio
from bilibiliClient import bilibiliClient
from PyQt5.QtWidgets import QApplication
import sys



app = QApplication(sys.argv)
danmuji = bilibiliClient()



tasks = [
            danmuji.connectServer() ,
            danmuji.HeartbeatLoop(),
            danmuji.show(),
            app.exec_()
        ]

loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(asyncio.wait(tasks))

except KeyboardInterrupt:
    danmuji.connected = False
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.run_forever()

loop.close()
