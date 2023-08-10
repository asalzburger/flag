import sys
import uproot
import numpy as np

MATERIAL_RECORDING_RESULTS = "data/closing_the_loop/geant4_material_tracks.root"
MATERIAL_RANGE_OUTPUT_FILE = "data/closing_the_loop/range.txt"

def main():
    matZ = readMaterialRecordings()
    materialArr = createSortedMaterialArray(matZ)
    outputMaterialRange(materialArr)

def readMaterialRecordings(filePath=MATERIAL_RECORDING_RESULTS):
    with uproot.open(filePath) as file:
        matZ = file["material-tracks/mat_Z"].array()
    return matZ

def createSortedMaterialArray(matZ):
    materials = set()
    for materialList in matZ:
        for material in materialList:
            materials.add(material)
    materialArr = np.array(list(materials))
    materialArr = np.sort(materialArr)
    return materialArr

def outputMaterialRange(materialArr, outputFile=MATERIAL_RANGE_OUTPUT_FILE):
    outputString = " ".join([str(materialArr[0]), str(materialArr[len(materialArr)-1])])
    with open(outputFile, "w") as f:
        f.write(outputString)


if __name__ == '__main__':
    sys.exit(main())