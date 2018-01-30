#-*-coding:utf-8 -*-
__author__ = 'Jy2881'

import arcpy
import numpy as np
import test

a = r"D:\workspace\python\coordinate\data.gdb\Estonia"
b = r"D:\workspace\python\coordinate\data.gdb\Estonia_Project"

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

