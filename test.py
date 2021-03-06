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

# 下面记录了一些控制点在两个坐标系下的空间直角坐标系的坐标值
## srcs of wgs_1984: (4972564.008823484, 1121896.1598812349, 3820629.5196759496)
# print(GCStoSRCS(116.353671, 39.942335, 6378137, 6356752.3142451793))
# print(SRCStoGCS(4972564.008823484, 1121896.1598812349, 3820629.5196759496, 6378137, 6356752.3142451793))

## srcs of beijing_1954: (4972662.865269649, 1121908.7088013135, 3820678.989418116)
# print(GCStoSRCS(116.353024,39.941999,6378245,6356863.0187730473))
# print(SRCStoGCS(4972662.865269649, 1121908.7088013135, 3820678.989418116, 6378245, 6356863.0187730473))

## srcs of Observatorio Meteorologico: (4973055.450426054, 1122059.9965219735, 3820308.1743461723)
# print(GCStoSRCS(116.340106, 39.944159, 6378388, 6356911.9461279465))
# print(SRCStoGCS(4973055.450426054, 1122059.9965219735, 3820308.1743461723, 6378388, 6356911.9461279465))

# 基于布尔莎的正算公式
def bursa(deltaX,deltaY,deltaZ,rX,rY,rZ,m,x1,y1,z1):
    m = m*1e-6
    rX, rY, rZ = rX/3600.0, rY/3600.0, rZ/1296000
    out=(1+m)*np.dot(np.array([[1.0,rZ,-rY],[-rZ,1.0,rX],[rY,-rX,1.0]]),np.array([[x1,y1,z1]]).reshape(3,1))+np.array([[deltaX,deltaY,deltaZ]]).reshape(3,1)
    return out

# 下面是正算公式的测试过程
# ---------------------------- transform from beijing to wgs (coordinate frame) -----------------------
# beijing_1954 to wgs_1984 after function: (4972946.05158608, 1120639.60857762, 3820602.7375601)
#  4972691.6710024, 1121767.10573683, 3820602.7375601
print(bursa(31.4, -144.3, -74.8, 0.0, 0.0, -0.814, -0.38, 4972662.865269649, 1121908.7088013135, 3820678.989418116))

# result to GCS: (116.35142392567941, 39.89608461627541, 60.736785356886685)
print(SRCStoGCS(4972691.6710024, 1121767.10573683, 3820602.7375601, 6378137, 6356752.3142451793))

# ---------------------------- transform from wgs to beijing (coordinate frame)-----------------------
# # wgs_1984 to beijing_1954 after function: (4972847.19234003, 1120627.08201484, 3820553.26783673)
# print(bursa(31.4, -144.3, -74.8, 0.0, 0.0, 0.814, -0.38, 4972564.008823484, 1121896.1598812349, 3820629.5196759496))
#
# # result to GCS: (116.35192381010654, 39.896420514879345, -157.22144303750247)
# # 116.353024,39.941999
# print(SRCStoGCS(4972847.19234003, 1120627.08201484, 3820553.26783673, 6378245, 6356863.0187730473))

# ---------------------------- transform from beijing to wgs (position vector) -----------------------
# # beijing_1954 to wgs_1984 after function: (4972438.69972944, 1122888.35637439, 3820602.7375601)
# print(bursa(31.4, -144.3, -74.8, 0.0, 0.0, -0.814, -0.38, 4972662.865269649, 1121908.7088013135, 3820678.989418116))
#
# # result to GCS: (116.3514250643087, 39.977484632830965, 60.68347694724798)
# # # 116.353671, 39.942335
# print(SRCStoGCS(4972438.69972944, 1122888.35637439, 3820602.7375601, 6378137, 6356752.3142451793))

# ---------------------------- transform from wgs to beijing (position vector) -----------------------
# # beijing_1954 to wgs_1984 after function: (4972339.84615829, 1122875.78510655, 3820553.26783673)
# print(bursa(31.4, -144.3, -74.8, 0.0, 0.0, -0.814, -0.38, 4972564.008823484, 1121896.1598812349, 3820629.5196759496))
# #
# # result to GCS: (116.35199849744957, 39.9778205314398, -48.295829547569156)
# # 116.353024,39.941999
# print(SRCStoGCS(4972339.84615829, 1122875.78510655, 3820553.26783673, 6378137.0, 6356752.3142451793))

# ---------------------------- transform from wgs to Observatorio Meteorologico (coordinate frame)-----------------------
# # wgs_1984 to Observatorio_Meteorologico after function: (5044184.8896977, 1202178.40460386, 3704203.69896322)
# print(bursa(148.635396, 339.470115, 157.265381, 32.87685, -76.963371, -32.622853, -8.204889, 4972564.008823484, 1121896.1598812349, 3820629.5196759496))
#
# # result to GCS: (112.2265983755533, 42.11368695258121, 1502.5996462674811)
# print(SRCStoGCS(5044184.8896977, 1202178.40460386, 3704203.69896322, 6378388, 6356911.9461279465))

# ---------------------------- transform from Observatorio Meteorologico to wgs (coordinate frame)-----------------------
# # wgs_1984 to Observatorio_Meteorologico after function: (5044667.97271479, 1202343.75861147, 3703870.35374768)
# print(bursa(148.635396, 339.470115, 157.265381, 32.87685, -76.963371, -32.622853, -8.204889, 4973055.450426054, 1122059.9965219735, 3820308.1743461723))
#
# # result to GCS: (112.2080890547692, 42.115382583957945, 1940.5548613620922)
# print(SRCStoGCS(5044667.97271479, 1202343.75861147, 3703870.35374768, 6378137, 6356752.3142451793))

# ---------------------------- transform from wgs to Observatorio Meteorologico (position vector)-----------------------
# # wgs_1984 to Observatorio_Meteorologico after function: (4901158.80006979, 1042274.44532169, 3937307.17546844)
# print(bursa(148.635396, 339.470115, 157.265381, -32.87685, 76.963371, 32.622853, -8.204889, 4972564.008823484, 1121896.1598812349, 3820629.5196759496))
#
# # result to GCS: (120.47085030952515, 37.716715225131566, 2439.8327648574486)
# print(SRCStoGCS(4901158.80006979, 1042274.44532169, 3937307.17546844, 6378388, 6356911.9461279465))

# ---------------------------- transform from Observatorio Meteorologico to wgs (position vector)-----------------------
# # wgs_1984 to Observatorio_Meteorologico after function: (4901658.59219339, 1042436.76190703, 3936997.83529763)
# print(bursa(148.635396, 339.470115, 157.265381, -32.87685, 76.963371, 32.622853, -8.204889, 4973055.450426054, 1122059.9965219735, 3820308.1743461723))
#
# # result to GCS: (120.45230116207114, 37.71868379420898, 2873.723738785833)
# print(SRCStoGCS(4901658.59219339, 1042436.76190703, 3936997.83529763, 6378137, 6356752.3142451793))