from mpmath import mp
import itertools
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
    

def count1s(testString)->int:
    '''10101->3'''
    a =len(testString)-len(testString.replace('1',''))
    return a
print(count1s('qw1er1t1'))

def convertnumbertobindigits(integerNumber,length=16)->str:
    '''12123 -> 0010111101011011'''
    print(str(integerNumber),format(integerNumber,'b').zfill(length))
    return format(integerNumber,'b').zfill(length)
    
print(convertnumbertobindigits(12123))
def combinationsOf1s(testString)->int:
    per=set(itertools.permutations(testString,3))
    for val in per:
        print(*val)
    print(len(per))
print(combinationsOf1s('12'))
def intStringTo2Bit(testString):
    return testString
print(intStringTo2Bit('123'))



#print (mp.pi,'len',len(mypi), mypi)
#firstmatch=mypi.find('21287')
#print("firstmatch",firstmatch)



