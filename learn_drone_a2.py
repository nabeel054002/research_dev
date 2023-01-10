from connect import a2

result = 0
#now to see how this file can actually run on the side while simultaneously grabbing external info

l=1000002
m=1000003
o=1000004

while(True):
    print("current result for drone a1 is", result)
    result = ((l+m+o)/3)
    a2.train(result)
    l+=1
    m+=1
    o+=1
