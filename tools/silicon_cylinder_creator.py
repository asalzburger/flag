import sys
import pyg4ometry
import numpy as np

VIEW_GEOMETRY = False
OUTPUT_FILE_GDML = "data/cylinder_g4/silicon_cylinder.gdml"
OUTPUT_FILE_GMAD = "data/cylinder_g4/silicon_cylinder.gmad"
SPACE_LENGTH = 1000
N_CYLINDERS = 1
M_LAYERS = 1
S_SEGMENTS = 1
RAW_SEGMENT_ANGLE = np.pi * 2 / S_SEGMENTS
if S_SEGMENTS == 1:
    ACTUAL_SEGMENT_ANGLE = RAW_SEGMENT_ANGLE
else:
    ACTUAL_SEGMENT_ANGLE = RAW_SEGMENT_ANGLE - 0.005 * np.pi
LAYER_THICKNESS = 1
SPACE_BETWEEN_LAYERS = 0.3
START_INNER_RADIUS = 44
DEFAULT_SPACE_WIDTH_LENGTH = 100
# Innermost to outermost
# CYLINDER_MATERIALS = ["G4_Si"]
CYLINDER_MATERIALS = ["G4_Si", "G4_Li", "G4_Al", "G4_Ti"]

def main():
    cc = CylinderCreator()
    cc.createSpace()
    cc.createCylinders()
    if VIEW_GEOMETRY:
        cc.visualizeGeometry()
    cc.writeGdmlFile()


class CylinderCreator:
    def __init__(self):
        self.reg = None
        self.wl = None

    def createSpace(self):
        # Registry to store gdml data
        self.reg = pyg4ometry.geant4.Registry()
        # world solid and logical
        neededSpaceWidth = 2 * (START_INNER_RADIUS + M_LAYERS * LAYER_THICKNESS + (M_LAYERS - 1) * SPACE_BETWEEN_LAYERS)
        if neededSpaceWidth >= DEFAULT_SPACE_WIDTH_LENGTH:
            spaceWidth = neededSpaceWidth + 10
        else:
            spaceWidth = DEFAULT_SPACE_WIDTH_LENGTH
        ws   = pyg4ometry.geant4.solid.Box("solid_box",spaceWidth,spaceWidth,SPACE_LENGTH,self.reg)
        self.wl   = pyg4ometry.geant4.LogicalVolume(ws,"G4_Galactic","space_volume",self.reg)
        self.reg.setWorld(self.wl.name)
        self.reg

    def createCylinders(self):
        centerCoordinate, cylinderLength = self.determineSpaceInfo()
        for i in range(N_CYLINDERS):
            self.placeCylinder(i, centerCoordinate, cylinderLength)
            centerCoordinate -= cylinderLength

    def placeCylinder(self, i, centerCoordinate, cylinderLength):
        cylNumberStr = str(i + 1)
        innerRadius = START_INNER_RADIUS
        for layer in range(M_LAYERS):
            layerIndexStr = str(layer + 1)
            innerRadius = round(innerRadius + SPACE_BETWEEN_LAYERS, 1)
            outerRadius = round(innerRadius + LAYER_THICKNESS, 1)
            for segment in range(S_SEGMENTS):
                segmentIndexStr = str(segment + 1)
                solidCylinderName = "solid_cylinder_{}_{}_{}".format(cylNumberStr, layerIndexStr, segmentIndexStr)
                segmentStartAngle = RAW_SEGMENT_ANGLE * segment

                c   = pyg4ometry.geant4.solid.Tubs(solidCylinderName,innerRadius,outerRadius,cylinderLength-0.05,segmentStartAngle,ACTUAL_SEGMENT_ANGLE,self.reg)
                
                material = CYLINDER_MATERIALS[layer % len(CYLINDER_MATERIALS)]
                logicalCylinderName = "logical_cylinder_{}_{}_{}".format(cylNumberStr, layerIndexStr, segmentIndexStr)
                c_l = pyg4ometry.geant4.LogicalVolume(c,material,logicalCylinderName,self.reg)

                physicalCylinderName = "physical_cylinder_{}_{}_{}".format(cylNumberStr, layerIndexStr, segmentIndexStr)
                c_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,centerCoordinate],c_l,physicalCylinderName,self.wl,self.reg)
            layer += 1
            innerRadius += 1

    def determineSpaceInfo(self):
        cylinderLength = SPACE_LENGTH / N_CYLINDERS
        if N_CYLINDERS > 1:
            startCenterCoordinate = (N_CYLINDERS - 1) / 2 * cylinderLength
        else:
            startCenterCoordinate = 0.0
        return (startCenterCoordinate, cylinderLength)

    def visualizeGeometry(self):
        v = pyg4ometry.visualisation.VtkViewer()
        v.addLogicalVolume(self.wl)
        v.addAxes(20)
        v.view()

    def writeGdmlFile(self):
        w = pyg4ometry.gdml.Writer()
        w.addDetector(self.reg)
        w.write(OUTPUT_FILE_GDML)
        # Make a quick bdsim job for the one component in a beam line
        w.writeGmadTester(OUTPUT_FILE_GMAD, OUTPUT_FILE_GDML)


if __name__ == '__main__':
    sys.exit(main())