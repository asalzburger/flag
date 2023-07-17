import pyg4ometry
import numpy as np

VIEW_GEOMETRY = False
OUTPUT_FILE_GDML = "data/cylinder_pyg4ometry/silicon_cylinder.gdml"
OUTPUT_FILE_GMAD = "data/cylinder_pyg4ometry/silicon_cylinder.gmad"

# Registry to store gdml data
reg  = pyg4ometry.geant4.Registry()

# world solid and logical
ws   = pyg4ometry.geant4.solid.Box("solid_box",100,100,1000,reg)
wl   = pyg4ometry.geant4.LogicalVolume(ws,"G4_Galactic","space_volume",reg)
reg.setWorld(wl.name)

# Cylinder placed at origin
c1   = pyg4ometry.geant4.solid.Tubs("solid_cylinder",44,45,1000,0,2*np.pi,reg)
c1_l = pyg4ometry.geant4.LogicalVolume(c1,"G4_Si","logical_cylinder",reg)
c1_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,0],c1_l,"physical_cylinder",wl,reg)

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
