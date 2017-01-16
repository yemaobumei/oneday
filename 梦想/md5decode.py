import hashlib
import sys

def decryptMD5(testHash):
        s = []
        while True:
                m = hashlib.md5()
                for c in s:
                        m.update(chr(c))
                hash = m.hexdigest()
                if hash == testHash:
                        return ''.join([chr(c) for c in s])
                wrapped = True
                for i in range(0, len(s)):
                        s[i] = (s[i] + 1) % 256
                        if s[i] != 0:
                                wrapped = False
                                break
                if wrapped:
                        s.append(0)

print decryptMD5('9ef1969d6ed8fc9a289ef6b0e48e13b6')
