import sys
import os
import pyg4ometry

DEFAULT_G4_INPUT_FILE = "data/cylinder_g4/silicon_cylinder.gdml"
OUTPUT_FILE_INP = "data/cylinder_fluka/silicon_cylinder.inp"
OUTPUT_FILE_FLAIR = "data/cylinder_fluka/silicon_cylinder.flair"

# Create a silicon tube
try:
    reader = pyg4ometry.gdml.Reader(sys.argv[1])
except:
    print(" ".join(["Using default input file", DEFAULT_G4_INPUT_FILE]))
    reader = pyg4ometry.gdml.Reader(DEFAULT_G4_INPUT_FILE)

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
# TODO Find a better way to do this?
with open(OUTPUT_FILE_FLAIR, "r") as f:
    flairText = f.read()
flairTextHalves = flairText.split(OUTPUT_FILE_INP)
correctedFlairText = "".join([flairTextHalves[0],
                              os.getcwd(),
                              "/",
                              OUTPUT_FILE_INP,
                              flairTextHalves[1]])
with open(OUTPUT_FILE_FLAIR, "w") as f:
    f.write(correctedFlairText)
