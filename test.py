#-*-coding:utf-8 -*-
__author__ = 'Jy2881'

import numpy as np
import math

# 从地理坐标系（GCS）到空间直角坐标系
def GCStoSRCS(B, L, a, b):
    e = math.sqrt((a**2-b**2)/a**2)
    # divided by 180 degree
    B = B/180.0
    L = L/180.0

    N = a/(math.sqrt(1-(e*(math.sin(B)))**2))
    X = N*math.cos(B)*math.cos(L)
    Y = N*math.cos(B)*math.sin(L)
    Z = N*(1-e**2)*math.sin(B)
    return X, Y, Z

# 从空间直角坐标系到地理坐标系（GCS）
def SRCStoGCS(X, Y, Z, a, b):
    theta = math.atan((a*Z)/(b*math.sqrt(X**2+Y**2)))
    eS = math.sqrt((a**2-b**2)/b**2)
    e = math.sqrt((a**2-b**2)/a**2)
    B = math.atan((Z+eS**2*b*(math.sin(theta)**3))/(math.sqrt(X**2+Y**2)-a*(e**2)*(math.cos(theta)**3)))
    N = a/(math.sqrt(1-(e*(math.sin(B)))**2))
    L = math.atan(Y/X)
    H = math.sqrt(X**2+Y**2)/math.cos(B) - N

    # multiply by 180 degree
    B = B*180
    L = L*180
    return B, L, H

"""
下面记录了一些控制点在两个坐标系下的空间直角坐标系的坐标值
首先Estonia的长短轴分别为：6378137， 6356752.3141403561
然后wgs84的长短轴分别为：6378137， 6356752.3142451793
"""

"""
Estonia的变换:
# # 测试数据为oid=1的点，纬度是：58.427294， 经度是： 22.955874
测试数据的结果是：x:5998017.067714913, y:769117.227411912, z:2021224.466671673
"""
# print(GCStoSRCS(58.427294, 22.955874, 6378137, 6356752.3141403561))
# print(SRCStoGCS(5998017.067714913, 769117.227411912, 2021224.466671673, 6378137, 6356752.3141403561))

# 基于布尔莎的正算公式
def bursa(deltaX, deltaY, deltaZ, rX, rY, rZ, m, x1, y1, z1):
    m = m*1e-6
    rX, rY, rZ = rX/3600.0, rY/3600.0, rZ/12960000
    out = (1+m)*np.dot(np.array([[1.0,rZ,-rY],[-rZ,1.0,rX],[rY,-rX,1.0]]),np.array([[x1,y1,z1]]).reshape(3,1))\
        +np.array([[deltaX,deltaY,deltaZ]]).reshape(3,1)
    return out

"""
Estonia的七参数：
dx: 0.055, dy: -0.541, dz: -0.185, rx: -0.0183, ry: 0.0003, rz: 0.007, ds: -0.014
布尔莎变换得到的结果是： 5998016.87446149， 769106.36869001， 2021228.66288846
然后在转为地理坐标系得到的经纬度结果是：58.427421114876914, 22.955554133651027, -0.1523610008880496
在arcmap中用project工具转换得到的结果是： 58.427297， 22.955856
这个wgs84所需要的空间直角坐标系坐标应该为：5998017.111180345, 769116.6233214383, 2021224.5669139372
"""
# print(bursa(0.055, -0.541, -0.185, -0.0183, 0.0003, 0.007, -0.014, 5998017.067714913, 769117.227411912, 2021224.466671673))
# print(SRCStoGCS(5998016.87446149, 769106.36869001, 2021228.66288846, 6378137, 6356752.3142451793))

# print(bursa(280.83679038385,57.495009802255,116.647652203164,2.938211271759/3600,3.529785370116/3600,
#             -4.710281764406/3600,0.6304723858,-2085738.7757,55037028697,2892977.6829))

eeeeeeee
