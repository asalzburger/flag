import sys
import pyg4ometry
import numpy as np

VIEW_GEOMETRY = False
OUTPUT_FILE_GDML = "data/cylinder_pyg4ometry/silicon_cylinder.gdml"
OUTPUT_FILE_GMAD = "data/cylinder_pyg4ometry/silicon_cylinder.gmad"
SPACE_LENGTH = 1000
N_CYLINDERS = 5
M_LAYERS = 16
LAYER_THICKNESS = 1
START_INNER_RADIUS = 44
DEFAULT_SPACE_WIDTH_LENGTH = 100
# Innermost to outermost
CYLINDER_MATERIALS = ["G4_Si", "G4_U", "G4_Au", "G4_Ag"]

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
        neededSpaceWidth = 2 * (START_INNER_RADIUS + M_LAYERS * LAYER_THICKNESS)
        if neededSpaceWidth > DEFAULT_SPACE_WIDTH_LENGTH:
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
            solidCylinderName = "solid_cylinder_{}_{}".format(cylNumberStr, layerIndexStr)
            innerRadius = round(innerRadius, 1)
            outerRadius = innerRadius + LAYER_THICKNESS
            c   = pyg4ometry.geant4.solid.Tubs(solidCylinderName,innerRadius,outerRadius,cylinderLength,0,2*np.pi,self.reg)
            
            material = CYLINDER_MATERIALS[layer % len(CYLINDER_MATERIALS)]
            logicalCylinderName = "logical_cylinder_{}_{}".format(cylNumberStr, layerIndexStr)
            c_l = pyg4ometry.geant4.LogicalVolume(c,material,logicalCylinderName,self.reg)

            physicalCylinderName = "physical_cylinder_{}_{}".format(cylNumberStr, layerIndexStr)
            c_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,centerCoordinate],c_l,physicalCylinderName,self.wl,self.reg)
            layer += 1
            innerRadius += 1

    def determineSpaceInfo(self):
        cylinderLength = SPACE_LENGTH / N_CYLINDERS
        if N_CYLINDERS > 1:
            if N_CYLINDERS % 2 == 1:
                startCenterCoordinate = (N_CYLINDERS - 1) / 2 * cylinderLength
            else:
                startCenterCoordinate = N_CYLINDERS / 2 * cylinderLength + cylinderLength / 2
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