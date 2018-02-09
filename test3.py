#-*-coding:utf-8 -*-
__author__ = 'Jy2881'

import numpy as np
import math

"""
下面记录了一些控制点在两个坐标系下的空间直角坐标系的坐标值
首先Estonia的长短轴分别为：6378137， 6356752.3141403561
然后wgs84的长短轴分别为：6378137， 6356752.3142451793
# da是两个椭球的场半轴之差，df是两个椭球的扁率倒数之差，f是扁率，f=(a-b)/a
# M是子午圈曲率半径，M=a*(1-e**2)/math.sqrt((1-e**2*(math.sin(B))**2))**3
"""
def bursa_full(deltaX, deltaY, deltaZ, rX, rY, rZ, m, L1,B1,a1,b1,a2,b2):
    e1 = math.sqrt((a1**2-b1**2)/a1**2)
    f1 = (a1-b1)/a1
    f2 = (a2-b2)/a2
    da = a1-b1
    df = 1/f1 - 1/f2
    M = a1*(1-e1**2)/math.sqrt((1-e1**2*(math.sin(B1))**2))**3
    N1 = a1/(math.sqrt(1-(e1*(math.sin(B1)))**2))

    array_1 = np.array([-math.sin(L1)/(N1*math.cos(B1)), math.cos(L1)/(N1*math.cos(B1)), 0,
                        -math.sin(B1)*math.cos(L1)/M, -math.sin(B1)*math.sin(L1)/M, math.cos(B1)/M]).reshape(2,3)
    array_2 = np.array([deltaX, deltaY, deltaZ]).reshape(3,1)
    array_3 = np.array([math.tan(B1)*math.cos(L1), math.tan(B1)*math.sin(L1), -1.0,
                        -math.sin(L1), math.cos(L1), 0.0]).reshape(2,3)
    array_4 = np.array([rX, rY, rZ]).reshape(3,1)
    array_5 = np.array([0,-N1*(e1**2)*math.sin(B1)*math.cos(B1)]).reshape(2,1)*m
    array_6 = np.array([0 ,0, N1*(e1**2)*math.sin(B1)*math.cos(B1)/(M*a1),
                        (2-(e1**2)*(math.sin(B1))**2)*math.sin(B1)*math.cos(B1)/(1-f1)]).reshape(2,2)
    array_7 = np.array([da, df]).reshape(2,1)
    result = np.dot(array_1,array_2) + np.dot(array_3,array_4) + array_5 + np.dot(array_6,array_7)
    return result

def bursa(deltaX, deltaY, deltaZ, rX, rY, rZ, m, L1,B1,a1,b1,a2,b2):
    e1 = math.sqrt((a1**2-b1**2)/a1**2)
    f1 = (a1-b1)/a1
    f2 = (a2-b2)/a2
    da = a1-b1
    df = 1/f1 - 1/f2
    M = a1*(1-e1**2)/math.sqrt((1-e1**2*(math.sin(B1))**2))**3
    N1 = a1/(math.sqrt(1-(e1*(math.sin(B1)))**2))

    array_1 = np.array([-math.sin(L1)/(N1*math.cos(B1)), math.cos(L1)/(N1*math.cos(B1)), 0,
                        -math.sin(B1)*math.cos(L1)/M, -math.sin(B1)*math.sin(L1)/M, math.cos(B1)/M,
                        math.cos(B1)*math.cos(L1), math.cos(B1)*math.sin(L1),math.sin(B1)]).reshape(3,3)
    array_2 = np.array([deltaX, deltaY, deltaZ]).reshape(3,1)
    array_3 = np.array([0, 0, f1*(math.sin(B1))**2/M, (1+f1*(math.cos(B1))**2)*math.sin(2*B1),
                        -(1-f1*(math.sin(B1))**2), a1*(1-f1*(math.cos(B1))**2)*(math.sin(B1))**2]).reshape(3,2)
    array_4 = np.array([da, df]).reshape(2,1)
    result = np.dot(array_1, array_2)+np.dot(array_3,array_4)
    return result

if __name__ == '__main__':
    x = bursa(0.055,-0.541,-0.185,-0.0183,0.0003,0.007,-0.014,22.955874,58.427294,6378137,6356752.3141403561,6378137,6356752.3142451793)
    y = bursa_full(0.055,-0.541,-0.185,-0.0183,0.0003,0.007,-0.014,22.955874,58.427294,6378137,6356752.3141403561,6378137,6356752.3142451793)
    print(y,x)