#-*-coding:utf-8 -*-
__author__ = 'Jy2881'

import arcpy
import sys
import os

control_point_in = ""
control_point_out = ""
match_field = ""

class controlPoint:
    def __init__(self, featureClass, field):
        # init the parameters
        self.featureClass = featureClass
        self.field = field
        self.basePath = os.path.split(self.featureClass)[0]
        self.name = os.path.split(self.featureClass)[1]

        # check the field exist and unique
        fieldList = arcpy.ListFields(self.featureClass)
        if self.field not in fieldList:
            arcpy.AddError("{0} is not included in {1}.".format(self.field, self.featureClass))
            sys.exit(1)

        self.value = []
        with arcpy.da.SearchCursor(self.featureClass, [self.field]) as cursor:
            i = 0
            for row in cursor:
                self.value.append(row[0])
                i += 1
        if set(self.value) != i:
            arcpy.AddError("{0} field in {1} is not unique.".format(self.field, self.featureClass))
            sys.exit(1)

    def addXY(self):
        arcpy.AddXY_management(self.featureClass)

    def equalClass(self, other):
        if len(list(set(self.value).difference(set(other.value)))) != 0:
            arcpy.AddError("The filed in {0} and {1} are not the same.".format(self.featureClass, other.featureClas))
            sys.exit(1)

    def sortByField(self):
        outputPath = "in_memory/%s"%self.name
        arcpy.Sort_management(self.featureClass, outputPath, self.value)
        return outputPath

class calculate(controlPoint):
    def __init__(self):
        self.past = self[0]
        self.forward = self[1]
