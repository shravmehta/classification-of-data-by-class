import csv
import math
import operator
from pymongo import MongoClient

 dimensions = 4
 k=5
# Handling Data
def loadDataSet():
    dataset = []
    client = MongoClient()
    mydb = client.wordCupDictionary my_collection = mydb.new_collection cursor = my_collection.find({})
    for document in cursor:
        line = [float(document['dim1']),float(document['dim2']),float(document['dim3']),
        dataset.append(line)
    return dataset

# Calculating Similarity
def euclideanDistance(x1, x2):
    distance = 0
    for x in range(dimensions):
        distance += pow((x1[x] - x2[x]), 2)
    return math.sqrt(distance)

def taxicab_distance(x1, x2):
    distance=0
    for x in range(dimensions):
        distance += math.fabs(x1[x]-x2[x]) return distance

# getting Neighbors
def getNeighbors(dataset, newData):
    eu_distances = []
    taxi_distances = []
    for x in range(len(dataset)):
eu_dist = euclideanDistance(dataset[x], newData) 6
 taxi_dist = taxicab_distance(dataset[x], newData) eu_distances.append((dataset[x], eu_dist)) taxi_distances.append((dataset[x], taxi_dist))
eu_distances.sort(key=operator.itemgetter(1)) taxi_distances.sort(key=operator.itemgetter(1)) eu_neighbors = []
taxi_neighbors = []
for x in range(k): eu_neighbors.append(eu_distances[x][0]) taxi_neighbors.append(taxi_distances[x][0])
return eu_neighbors,taxi_neighbors
# Response
def getResponse(neighbors): classVotes = {}
for x in range(len(neighbors)): response = neighbors[x][-1] if response in classVotes:
classVotes[response] += 1 else:
classVotes[response] = 1
sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True) return sortedVotes[0][0]
def getResponse(neighbors): classVotes = {}
for x in range(len(neighbors)): response = neighbors[x][-1] if response in classVotes:
classVotes[response] += 1 else:
classVotes[response] = 1
sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True) return sortedVotes[0][0]

dataset = loadDataSet()
a = []
newData = [590,300,670,60]
a = getNeighbors(dataset, newData) print("%d Nearest Neighbors Are:" % k) for neighbor in a:
print(neighbor)
eu_classResponse = getResponse(a[0])
taxi_classResponse = getResponse(a[1])
print("\n\nClass Response of Euclidean Distance: ", eu_classResponse) print("\n\nClass Response of Taxi cab Distance: ", taxi_classResponse)
