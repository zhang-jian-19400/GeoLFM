#coding=utf-8
import Predict
import Filter
import math

#获得损失函数
def loss (testdata,p,q):
    er=0;
    for u, i, rui in testdata:
      pui = Predict(u, i, p, q);
      er += abs(rui-pui);
    return er/len(testdata);

def precision(testdata,p,q):
    precision = 0
    caridset = set();
    for u, i, rui in testdata:#统计测试集中的所有用户
        caridset.add(u)
    personNum = 0
    precision = {}
    for n in [2, 5, 10, 15, 20, 25]:
        precision.setdefault(n, 0)
    for carid in caridset:#对每一个用户分析其准确率
        personNum += 1
        rnum = 0;
        Rlist = []
        for u, i, rui in testdata:
            if u == carid:
                rnum += 1;
                Rlist.append(i)
        rank = Predict.recommend(p,q,carid) #通过训练的模型，为cardID计算研究范围内的所有的访问概率，并从大到小排好顺序。
        rank = Filter.filterByPosition(carid,rank) #通过当前的地理位置，推荐周围的网格。
        for n in [2, 5, 10, 15, 20, 25]:
            rank1 = rank#[0:n]
            item = 0;
            for l in Rlist:
                if l in rank1:
                    item += 1.0;
            precision[n] += item / rnum
    for n in [2, 5, 10, 15, 20, 25]:
        print precision[n] / personNum

def mse(dp,testdata,p,q):
    length = len(testdata)
    mae = 0
    rmse = 0
    for car,cposition,nextposition in testdata:
        rank = Predict.recommend(dp,p, q, car,cposition)#filter approximate range.list-tuple
        gridset,rank = Filter.filterByPosition(dp,cposition, rank) # norm distribution

        maxvalue = 0
        for i,s in rank:
            if float(s)>maxvalue:
                maxvalue=float(s)
        if nextposition in gridset:
            for i,s in rank:
                if (i==nextposition) and (maxvalue!=0):
                    mae += abs(1-float(s)/maxvalue)
                    rmse += (1 - float(s) / maxvalue)**2
                    break
        else:
            mae+=1
            rmse+=1
    content =  "mae:"+str((float(mae)/length))+str('\n');
    content += "rmse"+str(math.sqrt(float(rmse)/length));
    dp.persitantCurrentPath(content)

def mse_car(testdata,p,q):
    ccar=""
    carmse=0
    count=0
    for car, cposition, nextposition in testdata:
        if ccar!=car: #跳到了另外一条记录
            if carmse!=0:
                print(math.sqrt(carmse/count))
            ccar=car
            carmse = 0
            count=0
        count+=1
        rank = Predict.recommend(p, q, ccar, cposition)  # filter approximate range.list-tuple
        gridset, rank = Filter.filterByPosition(cposition, rank)  # norm distribution
        maxvalue = 0
        for i, s in rank:
            if float(s) > maxvalue:
                maxvalue = float(s)
        if nextposition in gridset and maxvalue != 0:
            for i, s in rank:
                if i == nextposition:
                    carmse += abs(1 - float(s) / maxvalue)
                    #carmse += (1 - float(s) / maxvalue)**2
                    break
        else:
            carmse += 1
def precision(testdata,p,q):
    item = {};
    length = len(testdata)
    range = [100, 60, 30, 20, 10, 5]
    for n in range:
        item.setdefault(str(n), 0)
    for car,cposition,nextposition in testdata:
        rank = Predict.recommend(p, q, car,cposition)#filter approximate range.
        rank = Filter.filterByPosition(cposition, rank) # norm distribution
        nextposition = int(nextposition);
        position = [nextposition+252,nextposition-252,nextposition+1,nextposition-1] #在其周围的网格,扩充准确性的范围。
        flag = 1;
        for n in range:
            rank = rank[0:n]
            if(flag==1):
                flag = 0
                for nextposition in position:
                    if str(nextposition) in rank:
                        flag = 1
                        item[str(n)] += 1.0
                        break
    for n in range:
        print item[str(n)] / length