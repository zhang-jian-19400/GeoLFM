#coding=utf-8
import numpy as np
from DataProcess import DataProcess

DataProcess

def Predict(carid,gridid,p,q):
    if gridid not in q:
        return 0
    return np.dot(p[carid],q[gridid])

def recommend(dp,p,q,carid,cp):
    rank=dict()
    list = dp.getNeighbor(cp)  # some grid may not be visited by any carid.
    for i in list:  # i should get from file.
        pui = abs(Predict(carid,i,p,q))
        rank[i] = pui  #记录对该网格的兴趣度
    rank = sorted(rank.items(),key=lambda x:x[1],reverse=True)
    return rank

def PredictF(Pu,Q):
    list=[]
    rows =Q.shape[0]  #字典转数组麻烦
    for i in range(rows):
        list.append(np.dot(Q[i],Pu))
    return np.array(list)


def cal(p,q):
    rows = p.shape[0]
    cols = q.shape[0]
    listresult = []
    for i in p:
        list=[]
        for j in q:
            list.append(i*j)
        listresult.append(list)
    return np.array(listresult)

# the probability a driver visit a grid. --CF
def visitPosibility(carid,gridid,p,q):
    sim=0
    simscore=0
    if gridid not in q:
        return 0
    for i in p: # carid
        sss = similar(p,i,carid)
        sim += sss*abs(Predict(i, gridid, p, q))
        simscore += sss
    return sim/simscore

# according the distance relation. filter all points which is possible pickup. we know distance less than 2km.
def recommendxx(p,q,carid,cp):
    rank=dict()
    list = DataProcess.getNeighbor(cp)  # some grid may not be visited by any carid.
    for i in list:  # i should get from file.
        pui = visitPosibility(carid, i, p, q)
        rank[i] = pui  #记录对该网格的兴趣度
    rank = sorted(rank.items(),key=lambda x: x[1], reverse=True)
    return rank;

def similar(p,i,j):
    vec1 = p[i]
    vec2 = p[j]
    value = range(len(vec1))

    sum_vec1 = sum([vec1[i] for i in value])
    sum_vec2 = sum([vec2[i] for i in value])

    square_sum_vec1 = sum([pow(vec1[i], 2) for i in value])
    square_sum_vec2 = sum([pow(vec2[i], 2) for i in value])

    product = sum([vec1[i] * vec2[i] for i in value])

    numerator = product - (sum_vec1 * sum_vec2 / len(vec1))
    dominator = ((square_sum_vec1 - pow(sum_vec1, 2) / len(vec1)) * (square_sum_vec2 - pow(sum_vec2, 2) / len(vec2))) ** 0.5

    if dominator == 0:
        return 0
    result = numerator / (dominator * 1.0)

    return result