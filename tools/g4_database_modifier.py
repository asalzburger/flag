import sys

INPUT_FILE = "data/g4_material_database/g4_material_database.txt"
OUTPUT_FILE = "data/g4_material_database/g4_material_database.csv"
COLUMNS = "Z,Name,density(g/cm^3),I(eV)"

def main():
    # Copy the database text from
    # https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/Appendix/materialNames.html#simple-materials-elements
    # and put it into the input file (above).
    createDatabaseFile()

def createDatabaseFile():
    # Process the material text file
    info = []
    with open(INPUT_FILE, "r") as f:
        while True:
            line = removeNewRow(f.readline())
            print(line)
            if line == "":
                break
            info.append(line)
            for _ in range(3):
                skipRows(f, 2)
                line = removeNewRow(f.readline())
                print(line)
                info.append(line)
            skipRows(f, 1)

    # Write the materials to a CSV file
    with open(OUTPUT_FILE, "w") as f:
        f.write(COLUMNS + "\n")
        i = 0
        while i < len(info):
            f.write(",".join(info[i:i+4]))
            f.write("\n")
            i += 4

def removeNewRow(info):
    if info.endswith("\n"):
        return info[0:len(info)-1]
    return info

def skipRows(file, nRows):
    for _ in range(nRows):
        file.readline()


if __name__ == "__main__":
    sys.exit(main())