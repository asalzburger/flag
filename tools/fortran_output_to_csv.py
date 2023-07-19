import sys
import re

INPUT_FILE = "data/cylinder_fluka/fortran_output.txt"
OUTPUT_FILE = "data/cylinder_fluka/fluka_cylinder_data.csv"

def main():
    text = readFileText(INPUT_FILE)
    createCsv(OUTPUT_FILE, text)

def readFileText(inputFile):
    with open(inputFile, "r") as f:
        text = f.read()
    return text

def createCsv(outputFile, text):
    rows = text.split("\n")
    columns = getColumns(rows)
    dataRows = getDataRows(rows)
    writeCsvFile(columns, dataRows, outputFile)

def writeCsvFile(columns, dataRows, outputFile):
    with open(outputFile, "w") as f:
        f.write(",".join(columns) + "\n")
        for rowValues in dataRows:
            f.write(",".join(rowValues) + "\n")

def getColumns(rows):
    columns = re.findall(r"\s([\w.]+)", rows[0])
    return columns

def getDataRows(rows):
    data = rows[1:len(rows)-1]
    dataRows = [re.findall(r"\s+([\w.-]+)", row) for row in data]
    # If conversion to floats is needed
    # for i in range(len(dataRows)):
    #     dataRows[i] = [float(x) for x in dataRows[i]]
    return dataRows


if __name__ == "__main__":
    sys.exit(main())