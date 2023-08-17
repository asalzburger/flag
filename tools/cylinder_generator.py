import sys
import pyg4ometry
import pandas as pd
import json
import math
import numpy as np

G4_MATERIALS = "data/g4_material_database/g4_material_database.csv"
MATERIAL_MAP = "data/closing_the_loop/material-map-Z6.json"
SPACE_LENGTH = 1000
STARTING_INNER_RADIUS = 44
STARTING_OUTER_RADIUS = 45

def main():
    cc = CylinderCreator()
    cc.generateCylinder()

class CylinderCreator:
    def __init__(self):
        self.reg = self.reg = pyg4ometry.geant4.Registry()
        self.wl = None
        self.nCylinders = -1
        # TOD Make the program check how many files there are or something
        self.mLayers = 1
        self.sSegments = -1
        self.cylinderLength = -1
        self.segmentAngle = -1

    def generateCylinder(self):
        g4Materials = self.readMaterials()
        print(g4Materials)
        self.createMaterialLayer(g4Materials)

    def readMaterials(self, filePath=G4_MATERIALS):
        return pd.read_csv(filePath)

    def createMaterialLayer(self, g4Materials):
        with open(MATERIAL_MAP, "r") as f:
            matMap = json.load(f)
        self.setBinInfo()
        binZs = matMap["Surfaces"]["entries"][0]["value"]["material"]["data"]
        cylinderNumber = 1
        segmentNumber = 1
        maxMatThickness = -1
        innerRadius = STARTING_INNER_RADIUS
        outerRadius = STARTING_OUTER_RADIUS
        for binZ in binZs:
            for material in binZ:
                matZ = self.getMaterialZ(material)
                matThickness = self.getMaterialThickness(material)
                if matThickness > maxMatThickness:
                    maxMatThickness = matThickness
                g4Mat = g4Materials.iloc[matZ]["Name"]
                print(g4Mat)
                self.placeSegment(cylinderNumber, segmentNumber, g4Mat, matThickness, innerRadius)

    def placeSegment(self, cylinderNumber, segmentNumber, g4Mat, matThickness, innerRadius):
        segmentCenter = self.cylinderLength / 2 + cylinderNumber * self.cylinderLength
        solidCylinderName = "solid_cylinder_{}_{}".format(str(cylinderNumber), str(segmentNumber))
        outerRadius = innerRadius + matThickness
        segmentStartAngle = (segmentNumber - 1) * self.segmentAngle
        c   = pyg4ometry.geant4.solid.Tubs(solidCylinderName,innerRadius,outerRadius,self.cylinderLength-0.05,segmentStartAngle,self.segmentAngle,self.reg)

        logicalCylinderName = "logical_cylinder_{}_{}_{}".format(cylNumberStr, layerIndexStr, segmentIndexStr)
        c_l = pyg4ometry.geant4.LogicalVolume(c,g4Mat,logicalCylinderName,self.reg)

        physicalCylinderName = "physical_cylinder_{}_{}_{}".format(cylNumberStr, layerIndexStr, segmentIndexStr)
        c_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,centerCoordinate],c_l,physicalCylinderName,self.wl,self.reg)

    def setBinInfo(self, matMap):
        self.nCylinders = self.getNumberOfCylinders(matMap)
        self.sSegments = self.getNumberOfSegments(matMap)
        self.cylinderLength = SPACE_LENGTH / self.nCylinders
        self.segmentAngle = 2 * np.pi / self.sSegments - 0.005 * np.pi

    def getNumberOfSegments(self, matMap):
        return matMap["Surfaces"]["entries"][0]["value"]["material"]["binUtility"]["binningdata"][0]["bins"]

    def getNumberOfSegments(self, matMap):
        return matMap["Surfaces"]["entries"][0]["value"]["material"]["binUtility"]["binningdata"][1]["bins"]

    def getMaterialZ(self, mapMaterial):
        try:
            return math.floor(mapMaterial["material"][3])
        except:
            return -1

    def getMaterialThickness(self, material):
        try:
            return material["thickness"]
        except:
            return -1

if __name__ == '__main__':
    sys.exit(main())