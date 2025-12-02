import unittest

# Library we want to unit test
from parse_annotation import *
import subprocess

NoFile = str('nofile.xml')
TestFile = str('testfile.xml')

def writeTestFile(filename, infoDictList, includeName=True):
    try:             
        with open(filename, "w") as f:
            for infoDict in infoDictList:
                f.write("    <annotation>\n\
	    <folder>DronePics</folder>\n\
	    <filename>DJI_0089.JPG</filename>\n\
	    <path>/mnt/e/Pics/DronePics/DJI_0089.JPG</path>\n\
	    <source>\n\
		    <database>Unknown</database>\n\
	    </source>\n\
	    <size>\n\
		    <width>"+str(infoDict['width'])+"</width>\n\
		    <height>"+str(infoDict['height'])+"</height>\n\
		    <depth>"+str(infoDict['depth'])+"</depth>\n\
	    </size>\n\
	    <segmented>0</segmented>\n\
	    <object>\n")
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
        
        infoDictList = [{'width': width_in, 'height': height_in, 'depth': depth_in, 'name': name_in, 'xmin': xmin_in, 'ymin': ymin_in, 'xmax': xmax_in, 'ymax': ymax_in}]
        
        writeTestFile(TestFile, infoDictList  ymax_in)
        success, returnList = parseDronePicsXml(TestFile, speciesList)
        
        self.assertEqual(success, True)
        self.assertEqual(returnList[0]['width'],  infoDictList[0]['width'])
        self.assertEqual(returnList[0]['height'], infoDictList[0]['height'])
        self.assertEqual(returnList[0]['depth'],  infoDictList[0]['depth'])
        self.assertEqual(returnList[0]['name'],   infoDictList[0]['name'])
        self.assertEqual(returnList[0]['xmin'],   infoDictList[0]['xmin'])
        self.assertEqual(returnList[0]['ymin'],   infoDictList[0]['ymin'])
        self.assertEqual(returnList[0]['xmax'],   infoDictList[0]['xmax'])
        self.assertEqual(returnList[0]['ymax'],   infoDictList[0]['ymax'])
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
        
        infoDictList = [{'width': width_in, 'height': height_in, 'depth': depth_in, 'name': name_in, 'xmin': xmin_in, 'ymin': ymin_in, 'xmax': xmax_in, 'ymax': ymax_in}]
        writeTestFile(TestFile, infoDictList, False)
        success, width, height, depth, name, xmin, ymin, xmax, ymax, classid = parseDronePicsXml(TestFile, speciesList)
        
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
        
        infoDictList = [{'width': width_in, 'height': height_in, 'depth': depth_in, 'name': name_in, 'xmin': xmin_in, 'ymin': ymin_in, 'xmax': xmax_in, 'ymax': ymax_in}]
        
        width_in = 300
        height_in = 200
        depth_in = 3
        name_in = "Mesquite"
        xmin_in = 0
        ymin_in = 0
        xmax_in = 25
        ymax_in = 25
        speciesList = []
        
        infoDictList.append({'width': width_in, 'height': height_in, 'depth': depth_in, 'name': name_in, 'xmin': xmin_in, 'ymin': ymin_in, 'xmax': xmax_in, 'ymax': ymax_in})
        
        writeTestFile(TestFile, infoDictList  ymax_in)
        success, returnList = parseDronePicsXml(TestFile, speciesList)
        
        count = 0
        while count < len(infoDictList):
            self.assertEqual(success, True)
            self.assertEqual(returnList[count]['width'],  infoDictList[count]['width'])
            self.assertEqual(returnList[count]['height'], infoDictList[count]['height'])
            self.assertEqual(returnList[count]['depth'],  infoDictList[count]['depth'])
            self.assertEqual(returnList[count]['name'],   infoDictList[count]['name'])
            self.assertEqual(returnList[count]['xmin'],   infoDictList[count]['xmin'])
            self.assertEqual(returnList[count]['ymin'],   infoDictList[count]['ymin'])
            self.assertEqual(returnList[count]['xmax'],   infoDictList[count]['xmax'])
            self.assertEqual(returnList[count]['ymax'],   infoDictList[count]['ymax'])
            count = count + 1
            
        self.assertEqual(len(speciesList), 2)
        self.assertEqual(classid, 0)

if __name__ == '__main__':
    unittest.main()
