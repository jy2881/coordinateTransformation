#-*-coding:utf-8 -*-
__author__ = 'Jy2881'

import numpy as np
import math

def GCStoSRCS(B, L, a, b):
    e = math.sqrt((a**2-b**2)/a**2)
    N = a/(math.sqrt(1-(e*(math.sin(B)))**2))
    X = N*math.cos(B)*math.cos(L)
    Y = N*math.cos(B)*math.sin(L)
    Z = (N*(1-e**2)*math.sin(B))
    return X, Y, Z

def SRCStoGCS(X, Y, Z, a, b):
    theta = math.atan((a*Z)/(b*math.sqrt(X**2+Y**2)))
    eS = math.sqrt((a**2-b**2)/b**2)
    e = math.sqrt((a**2-b**2)/a**2)
    B = math.atan((Z+eS**2*b*(math.sin(theta)**3))/(math.sqrt(X**2+Y**2)-a*(e**2)*(math.cos(theta)**3)))
    N = a/(math.sqrt(1-(e*(math.sin(B)))**2))
    L = math.atan(Y/X)
    H = math.sqrt(X**2+Y**2)/math.cos(B) - N
    return B, L, H

# srcs of wgs_1984: (3946903.2582788575, -4957101.802873627, -725383.8819119472)
# print(GCStoSRCS(116.353671,39.942335,6378137,6356752.3142451793))
# srcs of beijing_1954: (3945595.650680904, -4958877.874843666, -721324.0275222213)

# print(GCStoSRCS(116.353024,39.941999,6378245,6356863.0187730473))
# print(SRCStoGCS(3945595.650680904, -4958877.874843666, -721324.0275222213,6378245,6356863.0187730473))

print(GCStoSRCS(12,20,100,20))
print(SRCStoGCS(34.436166334894835, 77.03924639325362, -53.657291800043495,100,20))

def bursa(deltaX,deltaY,deltaZ,rX,rY,rZ,m,x1,y1,z1):
    out = (1+m)*np.dot(np.array([[1,rZ,-rY],[-rZ,1,rX],[rY,-rX,1]]),np.array([[x1,y1,z1]]).reshape(3,1))+np.array([[deltaX,deltaY,deltaZ]]).reshape(3,1)
    return out

# ---------------------------- transform from beijing to wgs -----------------------
# beijing_1954 to wgs_1984 after function: (-56345.78245394,-5065911.79538871,-447295.69706378)
# print(bursa(31.4, -144.3, -74.8, 0.0, 0.0, 0.814, -0.38, 3945595.650680904, -4958877.874843666, -721324.0275222213))

# result to GCS: (-0.08879721485973409, 1.559674250182629, -1292040.4734170046)
# print(SRCStoGCS(-56345.78245394,-5065911.79538871,-447295.69706378,6378137,6356752.3142451793))

# ---------------------------- transform from wgs to beijing -----------------------
# wgs_1984 to beijing_1954 after function:
# print(bursa(31.4, -144.3, -74.8, 0.0, 0.0, 0.814, -0.38, 3946903.2582788575, -4957101.802873627, -725383.8819119472))

# result to GCS: (-0.08930220475661549, 1.5600102412263983, -1292382.7788294181)
# print(SRCStoGCS(-54638.71774137,-5065470.55416982,-449812.80678541,6378245,6356863.0187730473))

# ---------------------------- transform from beijing to wgs (position vector) -----------------------
# beijing_1954 to wgs_1984 after function: (4948947.18929826,-1083385.36941743,-447295.69706378)
# print(bursa(31.4, -144.3, -74.8, 0.0, 0.0, -0.814, -0.38, 3945595.650680904, -4958877.874843666, -721324.0275222213))

# result to GCS: (-0.08879866354200622, -0.2155125746292274, -1292122.5604539402)
# print(SRCStoGCS(4948947.18929826,-1083385.36941743,-447295.69706378,6378137,6356752.3142451793))