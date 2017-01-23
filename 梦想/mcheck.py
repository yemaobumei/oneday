import hashlib
# account	13126772351
# deviceId	5C8448A1-1D70-4541-A9D3-37187C1382CA
# mcheck	7a7063a7420e7d0462887e34ad8545ff
# password	9ef1969d6ed8fc9a289ef6b0e48e13b6
# r	1485160528374
r=1485160528374
x=hashlib.md5()
for i in range(100000):
	x.update(str(r))
	y=x.hexdigest()
	print y
	if y=='7a7063a7420e7d0462887e34ad8545ff':
		print r
		break
	r=r+1
print 'over'