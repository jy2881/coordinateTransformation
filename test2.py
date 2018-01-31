#-*-coding:utf-8 -*-
__author__ = 'Jy2881'

import arcpy
import numpy as np
import test

# 两个数据，a是EStonia1992坐标系的要素类，b是他转为wgs84坐标系后的数据要素类
a = r"D:\workspace\python\coordinate\data.gdb\Estonia"
b = r"D:\workspace\python\coordinate\data.gdb\Estonia_Project"

# 用来存储ax,ay,az,bx,by,bz
vector = [[],[],[],[],[],[]]

a_Estonia = 6378137
b_Estonia = 6356752.3141403561
a_wgs84 = 6378137
b_wgs84 = 6356752.3142451793

with arcpy.da.SearchCursor(a,["POINT_X","POINT_Y"]) as cursor:
    for row in cursor:
        result = test.GCStoSRCS(row[1], row[0], a_Estonia, b_Estonia)
        for i in range(0,3):
            vector[i].append(result[i])

with arcpy.da.SearchCursor(b,["POINT_X","POINT_Y"]) as cursor:
    for row in cursor:
        result = test.GCStoSRCS(row[1], row[0], a_Estonia, b_Estonia)
        for i in range(3,6):
            vector[i].append(result[i-3])

for i in range(0, len(vector[0])):
    if i == 0:
        B = np.array([[1, 0, 0, vector[0][i], 0, vector[2][i], -1*vector[1][i]],
                          [0, 1, 0, vector[1][i], -1*vector[2][i], 0, vector[0][i]],
                          [0, 0, 1, vector[2][i], vector[1][i], -1*vector[0][i], 0]])
        l = np.array([[vector[0][i]-vector[3][i]],
                      [vector[1][i]-vector[4][i]],
                      [vector[2][i]-vector[5][i]]])
    else:
        B = np.vstack((B, np.array([[1, 0, 0, vector[0][i], 0, vector[2][i], -1*vector[1][i]],
                          [0, 1, 0, vector[1][i], -1*vector[2][i], 0, vector[0][i]],
                          [0, 0, 1, vector[2][i], vector[1][i], -1*vector[0][i], 0]])))
        l = np.vstack((l, np.array([[vector[0][i]-vector[3][i]],
                                    [vector[1][i]-vector[4][i]],
                                    [vector[2][i]-vector[5][i]]])))

"""
求解七参数，文档中给的七参数应该是：
dx: 0.055, dy: -0.541, dz: -0.185, ds: -0.014， rx: -0.0183, ry: 0.0003, rz: 0.007
"""
x = np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), l) * np.array([[1], [1], [1], [1e6], [3600], [3600], [3600]])
print(x)
