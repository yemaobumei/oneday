import asyncio
import aiohttp
import json
loop = asyncio.get_event_loop()
sr=aiohttp.ClientSession(loop=loop) 
async def cont():
	with sr as s:
		async with s.get('https://account.bilibili.com/home/userInfo') as r:
			data = await r.text() #json.loads(r.text())
			js=json.loads(data)
			print(data,js['code'])


tasks = [
			cont()
		]

try:
	loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
	print('error')
	for task in asyncio.Task.all_tasks():
		task.cancel()
	loop.run_forever()

loop.close()
