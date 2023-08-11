import sys
import uproot
import numpy as np

# MATERIAL_RECORDING_RESULTS = "data/closing_the_loop/geant4_material_tracks.root"
# MATERIAL_RECORDING_RESULTS = "$HOME/builds/acts/Examples/Scripts/Python/geant4_material_tracks.root"
MATERIAL_RECORDING_RESULTS = "geant4_material_tracks.root"
# MATERIAL_RANGE_OUTPUT_FILE = "data/closing_the_loop/range.txt"
MATERIAL_RANGE_OUTPUT_FILE = "$HOME/Documents/CERN/Arbete/flag/data/closing_the_loop/range.txt"
# MATERIALS_OUTPUT_FILE = "$HOME/Documents/CERN/Arbete/flag/data/closing_the_loop/materials.txt"
MATERIALS_OUTPUT_FILE = "/home/taleiko/Documents/CERN/Arbete/flag/data/closing_the_loop/materials.txt"

def main():
    matZ = readMaterialRecordings()
    materialArr = createSortedMaterialArray(matZ)
    outputMaterials(materialArr)

def readMaterialRecordings(filePath=MATERIAL_RECORDING_RESULTS):
    with uproot.open(filePath) as file:
        matZ = file["material-tracks/mat_Z"].array()
    return matZ

def createSortedMaterialArray(matZ):
    materials = set()
    for materialArr in matZ:
        for material in materialArr:
            materials.add(material)
    materialArr = np.array(list(materials))
    materialArr = np.sort(materialArr)
    return materialArr

def outputMaterials(materialArrs, outputFile=MATERIALS_OUTPUT_FILE):
    with open(outputFile, "w") as f:
        f.write(" ".join([str(material) for material in materialArrs]))


if __name__ == '__main__':
    sys.exit(main())