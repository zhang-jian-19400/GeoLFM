# coding=utf-8
import random
import  numpy as np
import cPickle as cp
class DataProcess:

    def __init__(self,path):
        self.path=path

    def ReadShanghai(self):
      traindata=[];
      for line in open(self.path+'/SHTrain'):
        substrs = line.split('::')
        traindata.append((substrs[0], substrs[1], float(substrs[2])))
      return traindata

    def ReadShanghaiTest(self):
        testdata = [];
        for line in open(self.path+'/SHTest'):
            substrs = line.split('::')
            substrs[2] = substrs[2].replace("\n","");
            testdata.append((substrs[0], substrs[1], substrs[2]))
        return testdata

    def ReadShanghaiGrid(self):
        relationg2f = dict();
        for line in open(self.path+'/ClusterInfo'):
            substrs = line.split('::')
            id = substrs[0]
            substrs.pop(0);
            substrs.pop(-1)
            relationg2f[id] = [float(x) for x in substrs]
        return relationg2f

    def Dic2Array(self,t):
        list=[]
        for key in t:
            list.append(t[key])
        return np.array(list)

    #read visitMatrix to memory
    def ReadVisitMatrix(self):
        V={}
        for line in open(self.path+'/SHVisitByDistance'):
            v={}
            substrs = line.split(":")
            ssubstrs = substrs[1].split(",")
            for s in ssubstrs:
                sssubstrs = s.split(" ")
                if (len(sssubstrs)>1 and sssubstrs[1]!='\n'):
                    v.setdefault(str(sssubstrs[0]),sssubstrs[1])
            V[str(substrs[0])] = v
        return V



    def getNeighbor(self,id):
        neighbor = []
        for line in open(self.path+"/SHVisitByDistance"):
            substrs = line.split(":")
            if substrs[0] ==id:
                ssubstrs = substrs[1].split(",")
                for s in ssubstrs:
                    if s!="\n":
                        sssubstrs = s.split(" ")
                        neighbor.append(sssubstrs[0])
        return neighbor

    def load(self):
      p=q=dict();
      f = open(self.path+'/glfmp','r')
      p=cp.load(f);
      f.close()
      f = open(self.path+'/glfmq', 'r')
      q = cp.load(f);
      f.close()
      return p,q

    def persistant(self,p,q):
      f = open(self.path+'/glfmp', 'w')
      cp.dump(p, f);
      f.close()
      f = open(self.path+'/glfmq', 'w')
      cp.dump(q, f);
      f.close();

    def persitantCurrentPath(self,content):
        f = open(self.path+'/glfmresult','a')
        f.write(content)
        f.close();