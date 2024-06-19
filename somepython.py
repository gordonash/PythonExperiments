import numpy as np
import pandas as pd


msg="hello world"
print(msg,type(msg))

letters="".join([format(ord(letter),'b') for letter in msg])
print(letters,type(letters),type(letters[0]))
print(chr(int("1101000",2)))

nums=[num for num in range(0,32768)]

#print(nums)
ords=[(format(num,'b')).zfill(16) for num in nums]

#print(ords,len(ords))
print ('last:',ords[32767],'\n')
print(format(32767,'b'))
exit()


l=list()
l.append('a')
l.append('b')
l.append('b')
s=set()
s.add('a')
s.add('b')
s.add('b')
t=tuple()
t=tuple(s)
d=dict()
d['k1']=343
d['k1']=34322

print(l,s,t,d)
array=np.array(l)
print(type(array))
ba=bin(0b0001)

print(ba)
