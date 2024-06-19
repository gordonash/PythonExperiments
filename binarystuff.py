from mpmath import mp
s='z'
n=ord(s)
m=format(n,'b')
print(m,'yo')
mypi=str(mp.pi)

print(mypi,type(mypi))
a=mypi
numstrings=[format(i ,"b").zfill(8) for i in range(0,10)]
print(numstrings)
for i in range(0,10):
    a=a.replace(str(i),str(ord('a')+i))
    
print(a)
    




#print (mp.pi,'len',len(mypi), mypi)
#firstmatch=mypi.find('21287')
#print("firstmatch",firstmatch)



