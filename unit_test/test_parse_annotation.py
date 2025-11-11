import unittest

# Library we want to unit test
from parse_annotation import *
import subprocess

NoFile = str('nofile.xml')
TestFile = str('testfile.xml')

def writeTestFile(filename, width, height, depth, name, xmin, ymin, xmax, ymax, includeName=True):
    try:             
        with open(filename, "w") as f:
            f.write("    <annotation>\n\
	    <folder>DronePics</folder>\n\
	    <filename>DJI_0089.JPG</filename>\n\
	    <path>/mnt/e/Pics/DronePics/DJI_0089.JPG</path>\n\
	    <source>\n\
		    <database>Unknown</database>\n\
	    </source>\n\
	    <size>\n\
		    <width>"+str(width)+"</width>\n\
		    <height>"+str(height)+"</height>\n\
		    <depth>"+str(depth)+"</depth>\n\
	    </size>\n\
	    <segmented>0</segmented>\n\
	    <object>\n")
            if includeName:
                f.write("		    <name>" + str(name) + "</name>\n")
            
            f.write("<pose>Unspecified</pose>\n\
		    <truncated>0</truncated>\n\
		    <difficult>0</difficult>\n\
		    <bndbox>\n\
			    <xmin>"+str(xmin)+"</xmin>\n\
			    <ymin>"+str(ymin)+"</ymin>\n\
			    <xmax>"+str(xmax)+"</xmax>\n\
			    <ymax>"+str(ymax)+"</ymax>\n\
		    </bndbox>\n\
	    </object>\n\
    </annotation>\n")
    
    except FileNotFoundError as e:
        print("Error opening file: " + str(e))
        return 1
    except PermissionError as e:
        print("Error opening file: " + str(e))
        return 1
    except OSError as e:
        print("Error opening file: " + str(e))
        return 1
    return 0
    

class TestAddFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(["rm", "-f", NoFile])
        subprocess.run(["rm", "-f", TestFile])

    @classmethod
    def tearDownClass(cls):
        subprocess.run(["rm", "-f", NoFile])
        subprocess.run(["rm", "-f", TestFile])

    # This test shows no success from failed file 
    def test_failed_file_open(self):
        success, width, height, depth, name, xmin, ymin, xmax, ymax, classid = parseDronePicsXml(NoFile, [])
        self.assertEqual(success, False)

    def test_file_open(self):
        
        width_in = 400
        height_in = 300
        depth_in = 3
        name_in = "Mesquite"
        xmin_in = 1723
        ymin_in = 1060
        xmax_in = 2175
        ymax_in = 1495
        speciesList = []
        
        writeTestFile(TestFile, width_in, height_in, depth_in, name_in, xmin_in, ymin_in, xmax_in, ymax_in)
        success, width, height, depth, name, xmin, ymin, xmax, ymax, classid = parseDronePicsXml(TestFile, speciesList)
        
        self.assertEqual(success, True)
        self.assertEqual(width, width_in)
        self.assertEqual(height, height_in)
        self.assertEqual(depth, depth_in)
        self.assertEqual(name, name_in)
        self.assertEqual(xmin, xmin_in)
        self.assertEqual(ymin, ymin_in)
        self.assertEqual(xmax, xmax_in)
        self.assertEqual(ymax, ymax_in)
        self.assertEqual(len(speciesList), 1)
        self.assertEqual(classid, 0)

    def test_bad_format(self):
        
        width_in = 400
        height_in = 300
        depth_in = 3
        name_in = "Mesquite"
        xmin_in = 1723
        ymin_in = 1060
        xmax_in = 2175
        ymax_in = 1495
        speciesList = []
        
        writeTestFile(TestFile, width_in, height_in, depth_in, name_in, xmin_in, ymin_in, xmax_in, ymax_in, False)
        success, width, height, depth, name, xmin, ymin, xmax, ymax, classid = parseDronePicsXml(TestFile, speciesList)
        
        self.assertEqual(success, False)

if __name__ == '__main__':
    unittest.main()
