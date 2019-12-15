import numpy as np

# 读取特征数据文件
def readdata(filename):
    data = []
    f = open(filename, 'r')
    line = f.readline()
    num = 0
    while line:
        buf = list(map(float, line.split(',')))
        data.append(buf)
        line = f.readline()
        num = num + 1
    f.close()
    #data = np.array(data)  #读取的数据存储在数组中
    return data

#随机生成K个质心
def randomCenter(pointers,k):
    indexs = np.random.random_integers(0,len(pointers)-1,k)
    centers = []
    for index in indexs:
        centers.append(pointers[index])
    return centers

#计算两个向量的距离，用的是欧几里得距离
def distEclud(vecA, vecB):
    return np.sqrt(np.sum((vecA - vecB)**2))

#求这一组数据坐标的平均值,也就是新的质心
def getMean(data):
    Mean=[]
    for i in range (len(data[0])):
        means = np.mean(data[:,i])
        Mean.append(means)
    return Mean

def Save(data):
    data=np.array(data)
    f = open('sid_index.txt', 'w')
    for i in range(len(data)):
        f.write(str(data[i].astype(int)) + "\n")
    f.close

def KMeans(pointers,centers):
    diffAllNew = 1600
    diffAllOld = 0
    #afterClassfy = []
    while(abs(diffAllNew - diffAllOld)>0.0001):
        result=[]
        #更新diffAllOld为diffAllNEw
        diffAllOld = diffAllNew
        #先根据质心，对所有的数据进行分类
        afterClassfy = [[] for a in range(len(centers))]
        for pointer in pointers:
            dis = []
            for center in centers:
                pointer=np.array(pointer)
                center=np.array(center)
                dis.append(distEclud(pointer,center))
            minDis = min(dis)
            i=0
            for d in dis:
                if(minDis == d):
                    break
                else:
                    i += 1
            result.append(i+1)
            afterClassfy[i].append(pointer)
        afterClassfy = np.array(afterClassfy)
        #计算所有点到其中心距离的总的和
        diffAllNews = [[] for a in range(len(centers))]
        i=0
        for classs in afterClassfy:
            diffAllNews[i]=0
            for classss in classs:
                if len(classss) >0:
                    classss = np.array(classss)
                    center = np.array(centers[i])
                    diffAllNews[i] += distEclud(classss,center)
            i+=1
        diffAllNew = sum(diffAllNews)
        print(diffAllNew)
        #更新质心的位置
        i=0
        for classs in afterClassfy:
            classs = np.array(classs)
            if len(classs) > 0 :
                centers[i] = getMean(classs)
            #print(centers[i])
            i += 1
    return result

# 主函数
if __name__ == "__main__" :
    data=readdata("data.txt")
    centers=randomCenter(data,5)
    result=KMeans(data,centers)
    Save(result)