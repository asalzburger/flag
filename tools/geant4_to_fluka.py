import sys
import os
import pyg4ometry

OUTPUT_FILE_INP = "data/cylinder_fluka/silicon_cylinder.inp"
OUTPUT_FILE_FLAIR = "data/cylinder_fluka/silicon_cylinder.flair"

# Create a silicon tube
try:
    reader = pyg4ometry.gdml.Reader(sys.argv[1])
except:
    print("Please provide a pyg4ometry file for conversion.")
    sys.exit(0)
reg = reader.getRegistry()
logical = reg.getWorldVolume()
freg = pyg4ometry.convert.geant4Reg2FlukaReg(reg)
w = pyg4ometry.fluka.Writer()
w.addDetector(freg)
w.write(OUTPUT_FILE_INP)

# Create a Flair file with pyg4ometry's build-in function
extent = logical.extent(includeBoundingSolid=True)
f = pyg4ometry.fluka.Flair(OUTPUT_FILE_INP,extent)
f.write(OUTPUT_FILE_FLAIR)

# Correction of Flair input file path
# TODO DISGUSTING. Make this part better or find a better way to do it?
with open(OUTPUT_FILE_FLAIR, "r") as f:
    flairText = f.read()
flairTextHalves = flairText.split(OUTPUT_FILE_INP)
print(flairTextHalves)
correctedFlairText = "".join([flairTextHalves[0],
                              os.getcwd(),
                              "/",
                              OUTPUT_FILE_INP,
                              flairTextHalves[1]])
with open(OUTPUT_FILE_FLAIR, "w") as f:
    f.write(correctedFlairText)
print(correctedFlairText)