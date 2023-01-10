from connect import a3

result = 0
#now to see how this file can actually run on the side while simultaneously grabbing external info

l=100000000000000032
m=100000000000000033
o=100000000000000034

while(True):
    print("current result for drone a1 is", result)
    result = ((l+m+o)/3)
    a3.train(result)
    l+=1
    m+=1
    o+=1
