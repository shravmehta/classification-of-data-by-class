import math
from random import *
import numpy as np
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

def FCM_Step(X, V, c, m):
     n = len(X)
     p = len(X[0])
     # Fill the distance matrix
     dist = EuDistArrayOfVectors(V, X)
     # Calculate new U
     tmp = dist**(2/(m - 1))
     tmp2 = []
     #print(np.ones((c, 1)).dot((tmp**(-1)).sum(axis=0).T))
     for k in range(c):
         tmp2.append((tmp**(-1)).sum(axis=0))
     U = (tmp * tmp2)**(-1)

     for a in range(c):
         for b in range(n):
             if(np.isnan(U[a][b])):
                 U[a][b] = 1

    V_old = np.array(V)

    mf = U**m # MF matrix after exponential modification
    temp = []
    total = sum(mf.transpose())
    for i in range(p):
        temp.append(total)
    V = np.matmul(mf,X) / np.array(temp).transpose() # new center
    E = np.linalg.norm(np.subtract(V, V_old), ord=1)
    return [V, U, E]

def FCM_InitV(X, n, c):
# Initial cluster centers
# Assigning initial cluster centers
    V = []
    for i in range(c):
        V.append(dataset[randint(0,n-1)])
    return V

def fcm(X, c):
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
        V = init_V
    else:
        V = FCM_InitV(X, n, c)
    U = [[0]*c]*n
    iter_n = 0
    for i in range(max_iter):
        iter_n = i
        [V, T, E[i]] = FCM_Step(X, V, c, m) # check termination condition
        if E[i] <= term_thr:
            break
    for i in range(max_iter - iter_n):
        E.pop()
    return [V, U, E]

dataset = []
classes = []
U = []
init_V = []
V_new = []

[dataset, classes] = loadDataSet()
c=3

[V_new, U, E] = fcm(dataset, c)

print(V_new)
