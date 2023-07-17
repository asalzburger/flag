import sys
import pandas as pd
import re

BEG_FILE = "data/cylinder_fluka/fluka_beg.txt"
FLUKA_FILE = "data/cylinder_fluka/silicon_cylinder.inp"
GEOMETRY_ADDITIONS = "data/cylinder_fluka/geometry_additions.txt"
END_FILE = "data/cylinder_fluka/fluka_end.txt"
FILES_FIRST_HALF = [BEG_FILE, FLUKA_FILE]
FILES_SECOND_HALF = [END_FILE]
FLUKA_MATERIALS_CSV = "data/fluka_material_database/fluka_materials.csv"
MATERIALS = pd.read_csv(FLUKA_MATERIALS_CSV)

def main():
    textParts = createTextPartsList()
    writeCompletedFile(textParts)

def createTextPartsList():
    parts = [readFileText(file) for file in FILES_FIRST_HALF]
    parts.append(createMaterialPart())
    secondHalfParts = [readFileText(file) for file in FILES_SECOND_HALF]
    for part in secondHalfParts:
        parts.append(part)
    return parts

def createMaterialPart():
    materialPart = ""
    line = ""
    with open(FLUKA_FILE, "r") as f:
        text = f.read()
    for line in text.split("\n"):
        materialResults = searchForMaterialOnLine(line)
        if len(materialResults) > 0:
            print(line)
            materialNumber, materialId = getMaterialInfoFromLine(line)
            if materialNumber != -1:
                material = findMaterialInDatabase(materialNumber)
                materialPart += createMaterialRow(material, materialId)
    return materialPart

def searchForMaterialOnLine(line):
    return re.findall(r"MATERIAL", line)

def createMaterialRow(material, materialId):
    ident1 = float(material.Identifier_1)
    ident2 = float(material.Identifier_2)
    ident3 = float(material.Identifier_3)
    materialName = material.Name
    return "LOW-MAT, {}, {}, {}, {}, , , {}\n".format(materialId, ident1, ident2, ident3, materialName)

def findMaterialInDatabase(materialNumber):
    return MATERIALS[MATERIALS.Identifier_1 == materialNumber].iloc[0]

def getMaterialInfoFromLine(line):
    materialInfo = re.findall(r"MATERIAL,\s(\d+).\d*,\s[\d.]*,\s[\d.]*,\s[\d.]*,\s[\d.]*,\s[\d.]*,\s[\d.]*(\w+)", line)
    if len(materialInfo) > 0:
        return (int(materialInfo[0][0]), materialInfo[0][1])
    return (-1, -1)

def readFileText(filePath):
    with open(filePath, "r") as f:
        text = f.read()
    return text

def writeCompletedFile(textParts):
    with open(FLUKA_FILE, "w") as f:
        for part in textParts:
            print(part)
            f.write(part)
            f.write("\n\n")


if __name__ == "__main__":
    sys.exit(main())