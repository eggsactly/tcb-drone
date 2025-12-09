import unittest

# Library we want to unit test
from parse_annotation import *
import subprocess

NoFile = str('nofile.xml')
TestFile = str('testfile.xml')

def writeTestFile(filename, width, height, depth, infoDictList, includeName=True):
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
	    <segmented>0</segmented>\n")
            for infoDict in infoDictList:
                f.write("	    <object>\n")
                if includeName:
                    f.write("		    <name>" + str(infoDict['name']) + "</name>\n")
            
                f.write("<pose>Unspecified</pose>\n\
		    <truncated>0</truncated>\n\
		    <difficult>0</difficult>\n\
		    <bndbox>\n\
			    <xmin>"+str(infoDict['xmin'])+"</xmin>\n\
			    <ymin>"+str(infoDict['ymin'])+"</ymin>\n\
			    <xmax>"+str(infoDict['xmax'])+"</xmax>\n\
			    <ymax>"+str(infoDict['ymax'])+"</ymax>\n\
		    </bndbox>\n\
	    </object>\n")
            f.write("    </annotation>\n")
    
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
        success, width, height, depth, returnList = parseDronePicsXml(NoFile, [])
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
        
        infoDictList = [{'name': name_in, 'xmin': xmin_in, 'ymin': ymin_in, 'xmax': xmax_in, 'ymax': ymax_in, 'classID': 0}]
        
        writeTestFile(TestFile, width_in, height_in, depth_in, infoDictList)
        success, width, height, depth, returnList = parseDronePicsXml(TestFile, speciesList)
        
        self.assertEqual(success, True)
        self.assertEqual(width_in,  width)
        self.assertEqual(height_in, height)
        self.assertEqual(depth_in,  depth)
        self.assertEqual(returnList[0]['name'],   infoDictList[0]['name'])
        self.assertEqual(returnList[0]['xmin'],   infoDictList[0]['xmin'])
        self.assertEqual(returnList[0]['ymin'],   infoDictList[0]['ymin'])
        self.assertEqual(returnList[0]['xmax'],   infoDictList[0]['xmax'])
        self.assertEqual(returnList[0]['ymax'],   infoDictList[0]['ymax'])
        self.assertEqual(returnList[0]['classID'], infoDictList[0]['classID'])
        self.assertEqual(len(speciesList), 1)

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
        
        infoDictList = [{'name': name_in, 'xmin': xmin_in, 'ymin': ymin_in, 'xmax': xmax_in, 'ymax': ymax_in}]
        writeTestFile(TestFile, width_in, height_in, depth_in, infoDictList, False)
        success, width, height, depth, returnList = parseDronePicsXml(TestFile, speciesList)
        
        self.assertEqual(success, False)

    def test_multi_annotation(self):
        
        width_in = 400
        height_in = 300
        depth_in = 3
        name_in = "Mesquite"
        xmin_in = 1723
        ymin_in = 1060
        xmax_in = 2175
        ymax_in = 1495
        speciesList = []
        
        infoDictList = [{'name': name_in, 'xmin': xmin_in, 'ymin': ymin_in, 'xmax': xmax_in, 'ymax': ymax_in, 'classID': 0}]
        
        width_in = 300
        height_in = 200
        depth_in = 3
        name_in = "Palo Verde"
        xmin_in = 0
        ymin_in = 0
        xmax_in = 25
        ymax_in = 25
        speciesList = []
        
        infoDictList.append({'name': name_in, 'xmin': xmin_in, 'ymin': ymin_in, 'xmax': xmax_in, 'ymax': ymax_in, 'classID': 1})
        
        writeTestFile(TestFile, width_in, height_in, depth_in, infoDictList)
        success, width, height, depth, returnList = parseDronePicsXml(TestFile, speciesList)
        
        self.assertEqual(success, True)
        self.assertEqual(width_in,  width)
        self.assertEqual(height_in, height)
        self.assertEqual(depth_in,  depth)
        self.assertEqual(len(speciesList), 2)
        
        count = 0
        while count < len(infoDictList):
            self.assertEqual(returnList[count]['name'],    infoDictList[count]['name'])
            self.assertEqual(returnList[count]['xmin'],    infoDictList[count]['xmin'])
            self.assertEqual(returnList[count]['ymin'],    infoDictList[count]['ymin'])
            self.assertEqual(returnList[count]['xmax'],    infoDictList[count]['xmax'])
            self.assertEqual(returnList[count]['ymax'],    infoDictList[count]['ymax'])
            self.assertEqual(returnList[count]['classID'], infoDictList[count]['classID'])
            count = count + 1
        

if __name__ == '__main__':
    unittest.main()
