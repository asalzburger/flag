import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), "tools"))
import add_fluka_beg_and_end as a

MATERIAL_LINE = "MATERIAL, 14.0, 27.9769, 10.0, , , 28.0, M0000000\n"
NOT_MATERIAL_LINE = "COMPOUND, 0.9222961, M0000000, 0.04683195, M0000001, 0.03087197, M0000002, M00000\n"
LOW_MAT = "LOW-MAT, M0000000, 14.0, -2.0, 296.0, , , SILICON\n"

class addFlukaBegAndEndTest(unittest.TestCase):
    def test_recognizeMaterialLine(self):        
        searchResults = a.searchForMaterialOnLine(MATERIAL_LINE)
        self.assertEqual(len(searchResults), 1)
        searchResults = a.searchForMaterialOnLine(NOT_MATERIAL_LINE)
        self.assertEqual(len(searchResults), 0)

    def test_getMaterialInfoFromLine(self):
        materialNumber, materialId = a.getMaterialInfoFromLine(MATERIAL_LINE)
        self.assertEqual(materialNumber, 14)
        self.assertEqual(materialId, "M0000000")

    def test_findMaterialInDatabase(self):
        foundMaterial = a.findMaterialInDatabase(14)
        self.assertTrue(foundMaterial.any())

    def test_createMaterialRow(self):
        material = a.findMaterialInDatabase(14)
        materialRow = a.createMaterialRow(material, "M0000000")
        self.assertEqual(materialRow, LOW_MAT)

if __name__ == '__main__':
    unittest.main()