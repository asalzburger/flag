import sys

BEG_FILE = "data/cylinder_fluka/fluka_beg.txt"
FLUKA_FILE = "data/cylinder_fluka/silicon_cylinder.inp"
GEOMETRY_ADDITIONS = "data/cylinder_fluka/geometry_additions.txt"
END_FILE = "data/cylinder_fluka/fluka_end.txt"
FILES = [BEG_FILE, FLUKA_FILE, GEOMETRY_ADDITIONS, END_FILE]

def main():
    parts = [readFileText(file) for file in FILES]
    writeCompletedFile(parts)

def readFileText(filePath):
    with open(filePath, "r") as f:
        beginningText = f.read()
    return beginningText

def writeCompletedFile(textParts):
    with open(FLUKA_FILE, "w") as f:
        for part in textParts:
            f.write(part)
            f.write("\n\n")


if __name__ == "__main__":
    sys.exit(main())