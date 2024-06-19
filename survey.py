import pandas as pd
from mpmath import mp
column=['fred','alejandro','roger']

title_columns={"name":column,"height":[2,3,4],"weight":[343,43,22]}
print(title_columns)
data=pd.DataFrame(title_columns)
somestuff=data["weight"][1]
print(data)
print(somestuff)
somerow=data.iloc[2]
print (somerow)
mp.dps=100



mypi=str(mp.pi)
a=mypi
for i in range(0,10):
    a=a.replace(str(i),str(ord('a')+i))
    
print(a)
    




#print (mp.pi,'len',len(mypi), mypi)
#firstmatch=mypi.find('21287')
#print("firstmatch",firstmatch)



