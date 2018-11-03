# coding=utf-8
import numpy as np
import math
import Predict
import DataProcess
#创建训练集
p=q=dict()
def InitLFMGeo(datas,F):
    p=dict()
    q=dict()
    t=dict()
    for u,i,rui in datas:
        if not u in p:
            p[u] = np.random.rand(F)/math.sqrt(F)
        if not i in q:
            q[i] = np.random.rand(F)/math.sqrt(F)
    listkey = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']
    for k in range(0,5):
        t[listkey[k]] = np.random.rand(F)/math.sqrt(F)
    return (p,q,t)

def Initlfm(datas,F):
    p=dict()
    q=dict()
    t=dict()
    for u,i,rui in datas:
        if not u in p:
            p[u] = np.random.rand(F)/math.sqrt(F)
        if not i in q:
            q[i] = np.random.rand(F)/math.sqrt(F)
    for k in range(0,18):
        t[k] = np.random.rand(F)/math.sqrt(F)
    return (p,q,t)

def InitLFM(datas, F):
    p = dict();
    q = dict();
    for u, i, rui in datas:
        if not u in p:
            p[u] = np.random.rand(F) / math.sqrt(F);
        if not i in q:
            q[i] = np.random.rand(F) / math.sqrt(F);
    return (p, q)

# 加入了用户信息的矩阵分解方法
def LearningLFMGeo(train,relationg2f, F, n, alpha, lam1,lam2):
    (p,q,t) = InitLFMGeo(train,F)
    for step in range(0,n):
        totalerror = 0.0
        for u,i,rui in train:
            pui = Predict.Predict(u, i, p, q)
            eui = rui - pui;
            a=np.random.rand(F)/math.sqrt(F)
            b=0
            listkey=['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']
            listvalue = relationg2f[i]
            for j in range(0,5):
                value=listvalue[j]
                k = listkey[j]
                puii = Predict.Predict(i,k,q,t)
                euii = float(value) - puii
                t[k] += alpha *  ((lam2 * q[i] * euii) - lam1 * t[k])
                q[i] += alpha *  (p[u] * eui + lam2 * t[k] * (euii) - lam1 * q[i])
            p[u] += alpha * (q[i] * eui - lam1 * p[u])
            totalerror += np.abs(eui)
        print "error" + str(totalerror)
        alpha*=0.9
    return (p, q)

def LearningLFM(train, F, n, alpha, lam):
    (p, q) = InitLFM(train, F);
    for step in range(0, n):
        totalerror = 0.0;
        for u, i, rui in train:
            pui = Predict.Predict(u, i, p, q);
            eui = rui - pui;
            if eui>1:
                eui = 1;
            elif eui<-1:
                eui=-1;
            totalerror += np.abs(eui);
            p[u] += alpha * (q[i] * eui - lam * p[u]);
            q[i] += alpha * (p[u] * eui - lam * q[i]);
        print "error"+str(totalerror)
        alpha *= 0.9;
    return (p, q)

def geolfm1(A,X,epsilon,n):
    (p, q, t) = Initlfm(A,n)
    lam1=0.05
    alpha=0.05
    ep=100
    error = 0
    T = DataProcess.Dic2Array(t)
    while ep>epsilon:
        lasterror = error
        error =0
        for u, i, rui in A:
            # update p
            pui = Predict.Predict(u, i, p, q)-rui; #number
            Pu=np.array(p[u]);#get the u_th row in p
            Qi = np.array(q[i])
            Xi = np.array(X[i])
            Qp = Predict.PredictF(Pu,T)-Xi  #vector
            QpT = Predict.PredictF(Qp,T.T)
            p[u] = Pu-alpha*pui*Qi-lam1*alpha*QpT-lam1*alpha*Pu
            #update q
            q[i] = Qi-alpha*pui*Pu-lam1*alpha*Qi
            #update t
            QpPu = Predict.cal(Qp,Pu)
            T = T - alpha*lam1*QpPu-lam1*alpha*T
            error =error + np.abs(Predict.Predict(u, i, p, q)-rui)
        ep = np.abs(lasterror-error)
#       print "error"+str(error)
        alpha *= 0.9
    return (p,q)

def geolfm(dp,A,X,epsilon,n):
    (p, q, t) = Initlfm(A,n)
    lam1=0.05
    alpha=0.05
    ep=100
    error = 0
    T = dp.Dic2Array(t)
    while ep>epsilon:
        lasterror = error
        error =0
        for u, i, rui in A:
            try:
                # update p
                #p[u] = Pu-alpha*pui*Qi-lam1*alpha*QpT-lam1*alpha*Pu
                p[u] = p[u] - alpha*((np.dot(p[u],q[i])-rui)*q[i] + lam1*p[u]);
                #update q
    #            q[i] = Qi-alpha*pui*Pu-lam1*alpha*Qi
                q[i] = q[i] - alpha*((np.dot(p[u],q[i])-rui)*p[u] + lam1*np.dot((np.dot(q[i],T.T)-X[i]),T) +lam1*q[i])
                #update t
    #            T = T - alpha*lam1*QpPu-lam1*alpha*T
                qi = np.array(q[i])
                T = T - alpha*(np.dot(((np.dot(q[i],T.T)-X[i])).reshape(18,1),qi.reshape(1,n)) + lam1*T)
                error =error + np.abs((np.dot(p[u],q[i])-rui))
            except:
                print()
        ep = np.abs(lasterror-error)
#       print "error"+str(error)
        alpha *= 0.9
    return (p,q)

def lfm(A,epsilon):
    (p, q, t) = Initlfm(A,20)
    lam1=0.05
    alpha=0.05
    ep=100
    error = 0
    while ep>epsilon:
        lasterror = error
        error =0
        for u, i, rui in A:
            # update p
            p[u] = p[u] - alpha*(np.dot((np.dot(p[u],q[i])-rui),q[i]) + lam1*p[u])
            #update q
            q[i] = q[i] - alpha*(np.dot((np.dot(p[u],q[i])-rui),p[u]) + lam1*q[i])
            error =error + np.abs( Predict.Predict(u, i, p, q)-rui)
        ep = np.abs(lasterror-error)
#        print "error"+str(error)
        alpha *= 0.9
    return (p,q)

def train(dp,traindata,relationg2f,n):
    #融入了网格信息的矩阵分解
    #return LearningLFMGeo(traindata,relationg2f,10,50,0.07,0.01,0.01);
    #单纯的矩阵分解
    #return LearningLFM(traindata, 10, 50, 0.04, 0.01)
   return geolfm(dp,traindata,relationg2f,0.1,n)
#  return lfm(traindata,0.1)