import sys
import numpy as np
import math
from random import *
from pymongo import MongoClient

np.seterr(all='ignore')

def loadDataSet():
    dataset = []
    classes = []
    client = MongoClient("mongodb://localhost:27017")
    mydb = client.mydb
    my_collection = mydb.collection
    cursor = my_collection.find({})
    for document in cursor:
        line = [float(document['x1']),float(document['x2']),float(document['x3']),float(document['x4']]
        classes.append(document['class'])
        dataset.append(line)
    return [dataset, classes]

def EuDistArrayOfVectors (V, X):
    c = len(V)
    p = len(V[0])
    n = len(X)
    dist = np.zeros((c,n))
    V = np.array(V)
    X = np.array(X)
# fill the output matrix
    if p > 1:
        for k in range(c):
            temp = np.subtract(X, (np.ones((n,1)) * V[k]))**2
            temp = temp.sum(axis=1)
            dist[k] = np.sqrt(temp)
    else: # 1-D data
        for k in range(c):
            dist[k] = np.transpose(abs(np.subtract(V[k], X)))
    return dist

def PCM_InitV(X, n, c):
# Initial cluster centers
# Assigning initial cluster centers V = []
    for i in range(c):
        V.append(dataset[randint(0,n-1)])
    return V
def PCM_FindWeights(X, U, V, m, k):
# Find weights for PCM Clustering
    c = len(V)
    w = [0] * c

def PCM_Step(X, V, w, c, m):
     n = len(X)
     p = len(X[0])
# Fill the distance matrix
    dist = EuDistArrayOfVectors(V, X) # Calculate new T
    w = np.transpose(w)
    weights = [1/c]*n
    weights1 = []
    for i in range(c):
        weights1.append(weights)
    tmp = (dist**2) / weights1
    tmp = tmp ** ( 1/(m-1))
    T = 1 / (1 + tmp)

# For the situation of "singularity" (one of the data points is
# exactly the same as one of the cluster centers) T will be one.
    V_old = np.array(V)
    mf = T**m # MF matrix after exponential modification
    temp = []
    total = sum(mf.transpose())
    for i in range(p):
        temp.append(total)
    V = np.matmul(mf,X) / np.array(temp).transpose() # new center
    E = np.linalg.norm(np.subtract(V, V_old), ord=1)
    return [V, T, E]

def PCM(X, c, w):
"""if len(sys.argv) < 3:
        print("Too few input arguments !")
        return
    if len(sys.argv) > 5:
        print("Too many input arguments !")
        return"""
        n = len(X)
        p = len(X[0])
    # Change the following to set default options
    default_options = []
    default_options.append(2) # weighting exponent (m)
    default_options.append(100) # max number of iteration
    default_options.append(math.exp(1e-3)) # termination threshold
    default_options.append(1) # info display during iteration
    default_options.append(0) # use provided init_V

    options = default_options
    m = options[0] # Weighting exponent
    max_iter = options[1] # Max. iteration
    term_thr = options[2] # Termination threshold
    display = options[3] # Display info or not
    use_V_init = options[4] # use provided init_V

    if m <= 1:
        print("The weighting exponent should be greater than 1!")
        return
    E = [0] * max_iter # Array for termination measure values
    if use_V_init:
        V = V_init
    else:
        V = PCM_InitV(X, n, c)
    T = [[0]*c]*n
    iter_n = 0
    # Main loop
    for i in range(max_iter):
        iter_n = i
        [V, T, E[i]] = PCM_Step(X, V, w, c, m) # check termination condition
        if E[i] <= term_thr:
            break
    for i in range(max_iter - iter_n):
        E.pop()
    return [V, T, E]

dataset = []
classes = []
V_init = []
w = []
V_new = []
T = []
E = []

[dataset, classes] = loadDataSet()

c=3
# options = []
# Assigning initial cluster weights
for i in range(c):
    w.append(1/c)

[V_new, T, E] = PCM(dataset, c, w)
print(V_new)
