#coding=utf-8
#由于用户只会访问其周边的网格，所以我们需要筛选
import DataProcess

def filterByPosition(dp,cp,rank):
    # 得到这个用户访问过的元素，即他可能出现的位置
    V = dp.ReadVisitMatrix()
    tempRank = {}
    for i, s in rank:
        tempRank.setdefault(i,float(V[cp][i])*s) # 重新赋值
    rank = sorted(tempRank.items(), key=lambda x: x[1], reverse=True)
    # extract all grid
    rankResult =[]
    for i,s in rank:# i 是网格编号
            rankResult.append(i);
    return rankResult,rank#测试范围因素