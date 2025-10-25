# This python file is meant to be imported and used as a library for parsing
# the specific format of the photo annotations 

import xml.etree.ElementTree as ET

## parseDronePicsXml
#  Takes a path to an xml file as input and produces a tuple 
#  @param string path to xml file to parse
#  @param list of ints, classes is populated as this is parsed
#  @return success, 
def parseDronePicsXml(path, classes):
    success = True
    try:
        root = ET.parse(path).getroot()
    except FileNotFoundError:
        success = False

    return success 

