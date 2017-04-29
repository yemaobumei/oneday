import hashlib,time
deviceId='deviceId'
account='13126772351'
r=str(int(time.time()*1000))
u='/passport/login/AccountLoginAction.a'
md5 = hashlib.md5()
md5.update(u)
mcheck=md5.hexdigest()
print mcheck
