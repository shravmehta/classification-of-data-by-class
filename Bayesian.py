import xml.etree.ElementTree as ET
#parsing xml file to retrieve data
tree = ET.parse('classData1.xml') #get the root tag
root = tree.getroot()
#lists to store frequencies of data for class 1 and 2
f1 = []
f2 = []
#store classes according to data
c = []
#appending zero in lists at first
for i in range(1,101):
    f1.append(0)
    f2.append(0)
#Calculating frequency of data for each class
for i in range(1,3001):
    val = int(root[4][0][i-1][0][0].text)
    if int(root[4][0][i-1][1][0].text) == 1:
        f1[val-1] += 1
    else:
        f2[val-1] += 1
#Applying Bayesian theorem on frequencies of data
for i in range(1,101):
    f1[i-1] = (f1[i-1]/800) * (800/ 3000)
    f2[i-1] = (f2[i-1]/2200) * (2200/ 3000)
    temp = 1 if f1[i-1] > f2[i-1] else 2
    c.append(temp)
print (c)
#get boundary between classes

def getBoundry():
    for i in range(1,101):
        if(c[i-1] == 2):
            return i
def getClass(x):
    return c[x-1]
    
print(getBoundry())
