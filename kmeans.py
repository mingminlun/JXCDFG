from math import *
from numpy import *
import numpy as np
from numpy.ma import arccos
from cell_signal import distEclud

r = 6371229

'''
def distEclud(vecA, vecB):
    #return sqrt(
        ((vecA[0,0] - vecB[0,0]) * math.pi * r * math.cos(((vecA[0,1] + vecB[0,1]) / 2) * math.pi / 180
                                                      ) / 180) ** 2 + ((vecA[0,1] - vecB[0,1]) * math.pi * r / 180) ** 2
                                                      )
'''


def angle(lonA, latA, lonB, latB):
    angle0 = 0
    dx = lonA - lonB
    dy = latA - latB
    if dy == 0 and dx > 0:
        angle0 = 270
    elif dy == 0 and dx < 0:
        angle0 = 90
    else:
        x = abs(dx * pi * r * cos(((latA + latB) / 2) * pi / 180) / 180)
        y = abs(dy * pi * r / 180)
        angle0 = atan(x / y) * 180
        if dx > 0 > dy:
            angle0 = 360 - angle0
        elif dx >= 0 and dy > 0:
            angle0 = 180 + angle0
        elif dx < 0 < dy:
            angle0 = 180 - angle0
    return angle0


def angle_diff_0_180(ang1, ang2):
    tempAngleDiff = ang1 - ang2
    if 180 <= tempAngleDiff < 360:
        tempAngleDiff = 360 - tempAngleDiff
    elif 0 > tempAngleDiff >= -180:
        tempAngleDiff = abs(tempAngleDiff)
    elif -180 > tempAngleDiff >= -360:
        tempAngleDiff = 360 + tempAngleDiff
    return tempAngleDiff


def findCgi(vecA, database):
    distances = []  # 计算距离，保存dist,cgi,lon,lat,azimuth
    for line in database:
        distances.append(
            [distEclud(vecA[0, 0], vecA[0, 1], float(line[3]), float(line[4])),
             line[0], line[3], line[4], line[5]])
    try:
        shortestDist = sorted(distances, reverse=True)[-1][0]
    except IndexError:
        shortestDist = None
        print(vecA + 'cant find nearest cgi')
    nearestCells = []  # 选出最近的几个小区
    flag = True
    while flag:
        nearestCell = distances.pop()
        if nearestCell[0] == shortestDist:
            nearestCells.append(nearestCell)
        else:
            flag = False
    angles = []  # 计算最近小区的角度，保存角度，cgi
    for cell in nearestCells:
        angles.append([angle_diff_0_180(angle(vecA[0, 0], vecA[0, 1], cell[2], cell[3]), cell[4]), cell[1]])
    cgi = sorted(angles)[0][1]
    return cgi

def find_pts_cgi(pts,database):
    m = shape(pts)[0]
    ptsCgi = []
    for i in  range(m):





def distSLC(vecA, vecB):  # Spherical Law of Cosines
    a = math.sin(vecA[0, 1] * pi / 180) * sin(vecB[0, 1] * pi / 180)
    b = cos(vecA[0, 1] * pi / 180) * cos(vecB[0, 1] * pi / 180) * cos(pi * (vecB[0, 0] - vecA[0, 0]) / 180)
    return arccos(a + b) * r  # pi is imported with numpy


def randCent(dataSet, k):
    n = shape(dataSet)[1]  # 获取数据集第二维度
    centroids = np.mat(np.zeros((k, n)))
    # 构建簇质心
    for j in range(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * np.random.rand(k, 1)
    return centroids


def kMeans(dataSet, data_cgi_list, k, distMeas=distSLC, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    centroids = createCent(dataSet, k)
    centCgi = []
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf;
            minIndex = -1
            for j in range(k):
                # 寻找最近的质心
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI;
                    minIndex = j
            if clusterAssment[i:0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2
        # 更新质心位置
        print(centroids)
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment


def biKmeans(dataSet, cgiList, k, cellBase, distMeas=distSLC):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    # 创建初始簇
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList = [centroid0]
    centCgi = [findCgi(centroid0, cellBase)]
    for j in range(m):
        if cgiList[j] == centCgi[0]:
            clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :]) ** 2 * 0.8  # sse计算系数
        else:
            clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :]) ** 2
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            # 尝试划分每一簇
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:, 0].A == i)[0], :]
            cgiInCurrCluster = cgiList[nonzero(clusterAssment[:, 0].A == i)[0]]
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, cgiInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:, 1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != i)[0], 1])
            print("sseSplit, and notSplit: ", sseSplit, sseNotSplit)
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
                # 更新簇的分配结果
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        print('the bestCentToSplit is: ', bestCentToSplit)
        print('the len of bestClustAss is: ', len(bestClustAss))
        centList[bestCentToSplit] = bestNewCents[0, :]
        centList.append([bestNewCents[1, 0].tolist(), bestNewCents[1, 1].tolist()])
        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0], :] = bestClustAss
    return centList, clusterAssment
