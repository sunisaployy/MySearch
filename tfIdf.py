import math
from itertools import groupby

def dfFunctions(words,dicted,N,data):
    df = {}
    sim = {}
    for i in words:
        df[i] = {len(dicted[i])}
    idf = idfFunctions(words,df,N)
    tfidf = tfIdfFunctions(dicted,words,idf,data)

    if len(words) > 1:
        sim = countFunctions(tfidf,words)
    else:
        sim = tfidf[words[0]]
    return sim

def countFunctions(tfidf,words):
    sim = {}
    c = 0
    for i in range(1,101):
        for j in words:
            c = c + tfidf[j][i]
        sim[i] = c
        c = 0
    return sim

def idfFunctions(words,df,N):
    idf = {}
    for i in words:
        for j in df[i]:
            idf[i] = math.log(N/j,10)
    return idf

def tfIdfFunctions(dicted,words,idf,data):
    tfIdf = {}
    for i in words:
        for j in range(0,len(data)):
            a = data[j]
            if i in tfIdf:
                tfIdf[i][j+1] = a.count(i)*idf[i]
            else:
                tfIdf[i] =  j+1
                tfIdf[i] = {j+1 : a.count(i)*idf[i]}
    return tfIdf