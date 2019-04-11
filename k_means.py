import math
import operator
import numpy as np
from random import *
from pymongo import MongoClient

k=3
t_max = 25
max_error = 2
dimensions = 4

def loadDataSet():
    dataset = []
    classes = []
    client = MongoClient("mongodb://localhost:27017") mydb = client.mydb
    my_collection = mydb.collection
    cursor = my_collection.find({})
    for document in cursor:
        line = [float(document['x1']),float(document['x2']),float(document['x3']),float(classes.append(document['class'])
        dataset.append(line)
    return [dataset, classes]

def twoNorm(x):
     total = 0
     for i in range(len(x)):
         total += (x[i] * x[i])
     return math.sqrt(total)

def euclideanDistance(x1, x2):
    distance = 0
    for x in range(dimensions):
        distance += pow((x1[x] - x2[x]), 2)
    return math.sqrt(distance)

def calculateMinDistance(data, V):
     index = 0
     distances = []
     for centroid in V:
        distances.append((euclideanDistance(data, centroid), index))
        index+=1
     distances.sort(key=operator.itemgetter(0))
     return distances[0][1]

def calculateCentroids(dataset, V):
    Ut = np.zeros((k,len(dataset)), dtype=int)
    for i in range(len(dataset)):
        Ut[calculateMinDistance(dataset[i], V), i] = 1
    V_New = []
    for i in range(k):
        point_sum = [0] * dimensions
        counts = [0] * k
        for j in range(len(dataset)):
            if j == 0:
                point_sum = [0] * dimensions
            if(Ut[i][j] == 1):
                point_sum = [x+y for x, y in zip(point_sum, dataset[i])]
                counts[i] += 1
            if counts[i] != 0:
                V_New.append([x/counts[i] for x in point_sum])
            else:
                 V_New.append(V[i])
    return [Ut, V_New]

dataset = []
classes = []
V_init = []
V_new = []
Ut = []
[dataset, classes] = loadDataSet()

for i in range(k):
    V_init.append(dataset[randint(0,len(dataset)-1)])
for i in range(t_max):
    [Ut, V_new] = calculateCentroids(dataset,V_init)
    x = [0] * k
    for j in range(k):
        x[j] = euclideanDistance(V_init[j],V_new[j])
    V_init = V_new
    error = twoNorm(x)
    print(error)
    if error < max_error:
        break

print("\nCentroids: ", V_init)
for i in range(k):
    print("\nCluster ",i+1,":")
    Iris_virginica = 0
    Iris_versicolor = 0
    Iris_sentosa = 0
    for j in range(len(dataset)):
        if(Ut[i][j] == 1):
            if classes[j] == 'Iris-virginica':
                Iris_virginica += 1
            elif classes[j] == 'Iris-versicolor':
                Iris_versicolor += 1
            else:
                Iris_sentosa += 1
    print("Iris-verginica: ",Iris_virginica,"\nIris-versicolor: ",Iris_versicolor,"\nIris_sentosa",Iris_sentosa)
