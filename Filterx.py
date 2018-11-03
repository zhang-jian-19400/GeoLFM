#coding=utf-8
#由于用户只会访问其周边的网格，所以我们需要筛选

def filterByPosition(carid,rank):
    # 得到这个用户访问过的元素，即他可能出现的位置
    list = []
    last=0
    gridset = set()
    #通过当前的cardid ,获得历史上该carid去过的list
    for line in open('../data/beijing/currentRecord'):
        substrs = line.split("::")
        if substrs[0] == carid:
            if substrs[1]!="":
                last = str(substrs[1]).replace('\n','')
                break
    list.append(last)#通过最后一条记录获得，最近的位置信息
    #依次获得网格grid 周边范围内的网格存入到gridset中
    for grid in list:
        #str(gird).replace("grid", "")
        girdid = int(grid)
        i=0
        try:
            i = (girdid / 1000)
        except:
            print "error"
        file = "../data/nabor/beijing/gridneibor" + str(i)
        for line in open(file):
            substrs = line.split("::")
            if substrs[0] == grid:
                ssubstrs = substrs[1].split(" ")
                for strs in ssubstrs:
                    if strs != '\n':
                        gridset.add(strs)
#    return gridset
    #在得到近邻矩阵后，我们进行下步操作

    rankResult =[]
    for i,s in rank:# i 是网格编号
        if i in gridset:
            rankResult.append(i);
    return rankResult#测试范围因素



