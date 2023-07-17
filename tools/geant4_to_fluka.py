import sys
import pyg4ometry

OUTPUT_FILE_INP = "data/cylinder_fluka/silicon_cylinder.inp"
OUTPUT_FILE_FLAIR = "data/cylinder_fluka/silicon_cylinder.flair"

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

extent = logical.extent(includeBoundingSolid=True)
f = pyg4ometry.fluka.Flair(OUTPUT_FILE_INP,extent)
f.write(OUTPUT_FILE_FLAIR)

# EXPERIMENTAL
# with open(OUTPUT_FILE_FLAIR, "r") as f:
#     flairExtension = f.read()

# with open(OUTPUT_FILE_INP, "r") as f:
#     flukaText = f.read()

# with open(OUTPUT_FILE_FLAIR, "w") as f:
#     f.write(flukaText)
#     f.write(flairExtension)