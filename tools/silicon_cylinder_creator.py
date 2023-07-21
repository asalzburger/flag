import pyg4ometry
import numpy as np

VIEW_GEOMETRY = False
OUTPUT_FILE_GDML = "data/cylinder_pyg4ometry/silicon_cylinder.gdml"
OUTPUT_FILE_GMAD = "data/cylinder_pyg4ometry/silicon_cylinder.gmad"
N_CYLINDERS = 5
SPACE_LENGTH = 1000

# Registry to store gdml data
reg  = pyg4ometry.geant4.Registry()

# world solid and logical
ws   = pyg4ometry.geant4.solid.Box("solid_box",100,100,SPACE_LENGTH,reg)
wl   = pyg4ometry.geant4.LogicalVolume(ws,"G4_Galactic","space_volume",reg)
reg.setWorld(wl.name)

# Original cylinder placed at origin
# c1   = pyg4ometry.geant4.solid.Tubs("solid_cylinder_1",44,45,1000,0,2*np.pi,reg)
# c1_l = pyg4ometry.geant4.LogicalVolume(c1,"G4_Si","logical_cylinder_1",reg)
# c1_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,0],c1_l,"physical_cylinder_1",wl,reg)

# 4 smaller cylinders, automated
# Setting up things for cylinder creation
centerCoordinate = 0
if N_CYLINDERS > 1:
    cylinderLength = SPACE_LENGTH / N_CYLINDERS
    if N_CYLINDERS % 2 == 1:
        centerCoordinate = (N_CYLINDERS - 1) / 2 * cylinderLength
    else:
        centerCoordinate = N_CYLINDERS / 2 * cylinderLength + cylinderLength / 2

# Place the cylinders
for i in range(N_CYLINDERS):
    cylNumberStr = str(i + 1)
    c   = pyg4ometry.geant4.solid.Tubs("solid_cylinder_{}".format(cylNumberStr),44,45,cylinderLength,0,2*np.pi,reg)
    c_l = pyg4ometry.geant4.LogicalVolume(c,"G4_Si","logical_cylinder_{}".format(cylNumberStr),reg)
    c_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,centerCoordinate],c_l,"physical_cylinder_{}".format(cylNumberStr),wl,reg)
    centerCoordinate -= cylinderLength

# Visualise geometry
v = pyg4ometry.visualisation.VtkViewer()
v.addLogicalVolume(wl)
v.addAxes(20)
if VIEW_GEOMETRY:
    v.view()

w = pyg4ometry.gdml.Writer()
w.addDetector(reg)
w.write(OUTPUT_FILE_GDML)
# Make a quick bdsim job for the one component in a beam line
w.writeGmadTester(OUTPUT_FILE_GMAD, OUTPUT_FILE_GDML)
