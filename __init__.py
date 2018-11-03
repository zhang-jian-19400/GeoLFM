#coding=utf-8
from DataProcess import DataProcess
import Evaluate
import Geo_LFM
import datetime
import os
if __name__=="__main__":

    rootdir = '../data/'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.exists(path):
            dp = DataProcess(path)
            TrainData = dp.ReadShanghai()
            TestData = dp.ReadShanghaiTest()
            gridFeatrue = dp.ReadShanghaiGrid()
            #10,15,20,25,30,35,40,45,50,60,70,80,100,120,150,200,250,300,
            for n in [20]:
                print("开始训练。。。")
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                p, q = Geo_LFM.train(dp,TrainData,gridFeatrue,n)
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print("训练完毕，持久化结果")
        #        dp.persistant(p, q)
                #p,q = dp.load()
                print("验证结果")
                Evaluate.mse(dp,TestData, p, q)
