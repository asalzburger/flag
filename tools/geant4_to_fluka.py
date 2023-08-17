import sys
import os
import pyg4ometry
from silicon_cylinder_creator import CylinderCreator

DEFAULT_G4_INPUT_FILE = "data/cylinder_g4/silicon_cylinder.gdml"
OUTPUT_FILE_INP = "data/cylinder_fluka/silicon_cylinder.inp"
OUTPUT_FILE_FLAIR = "data/cylinder_fluka/silicon_cylinder.flair"
READ_GEOMETRY_FROM_FILE = True

def main():
    if READ_GEOMETRY_FROM_FILE:
        convertGeometryFromFile()
    else:
        convertGeometryWithoutFile()

def convertGeometryFromFile():
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
    createFlairFile(logical)
    flairInputPathCorrection()

# TODO
# Currently this part leads to the geometry being created two times
# since it is already created in silicon_cylinder_creator earlier
# in the pipeline.
# Consider making changes if this part is used in a larger context
# and the program is run many times for time and computing
# efficiency.
def convertGeometryWithoutFile():
    cc = CylinderCreator()
    cc.createSpace()
    # Note that the number of cylinders, layers and segments is
    # currently set in the file silicon_cylinder_creator.py
    cc.createCylinders()

    reg = cc.reg
    logical = reg.getWorldVolume()
    freg = pyg4ometry.convert.geant4Reg2FlukaReg(reg)
    w = pyg4ometry.fluka.Writer()
    w.addDetector(freg)
    w.write(OUTPUT_FILE_INP)
    createFlairFile(logical)
    flairInputPathCorrection()

    # freg = pyg4ometry.convert.geant4Reg2FlukaReg(cc.reg)
    # w = pyg4ometry.fluka.Writer()
    # w.addDetector(freg)
    # w.write(OUTPUT_FILE_INP)
    # createFlairFile(cc.reg.getWorldVolume())
    # flairInputPathCorrection()

def createFlairFile(logical):
    # Create a Flair file with pyg4ometry's built-in function
    extent = logical.extent(includeBoundingSolid=True)
    f = pyg4ometry.fluka.Flair(OUTPUT_FILE_INP,extent)
    f.write(OUTPUT_FILE_FLAIR)

def flairInputPathCorrection():
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


if __name__ == "__main__":
    sys.exit(main())