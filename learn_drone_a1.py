from connect import a1

result = 0
#now to see how this file can actually run on the side while simultaneously grabbing external info

l=12
m=13
o=14

while(True):
    print("current result for drone a1 is", result)
    result = ((l+m+o)/3)
    a1.train(result)
    l+=1
    m+=1
    o+=1
