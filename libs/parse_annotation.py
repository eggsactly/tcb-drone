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
    width = 0
    height = 0
    depth = 0
    name = ''
    xmin = 0
    ymin = 0
    xmax = 0
    ymax = 0
    classid = -1
    
    try:
        root = ET.parse(path).getroot()
    except FileNotFoundError:
        success = False

    if success:
        if len(root.findall('size')) > 0:
            type_tag = root.findall('size')
            try:
                width = int(type_tag[0].findall('width')[0].text)
                height = int(type_tag[0].findall('height')[0].text)
                depth = int(type_tag[0].findall('depth')[0].text)
            except IndexError:
                success = False
        else:
            success = False
        if len(root.findall('object')) > 0:
            type_tag = root.findall('object')
            try:
                name = str(type_tag[0].findall('name')[0].text)
                if name in classes:
                    classid = classes.index(name)
                else:
                    classes.append(name)
                    classid = len(classes) - 1
            except IndexError:
                success = False
                
            if len(root.findall('object')[0].findall('bndbox')) > 0:
                type_tag = root.findall('object')[0].findall('bndbox')
                try:
                    xmin = int(type_tag[0].findall('xmin')[0].text)
                    ymin = int(type_tag[0].findall('ymin')[0].text)
                    xmax = int(type_tag[0].findall('xmax')[0].text)
                    ymax = int(type_tag[0].findall('ymax')[0].text)
                except IndexError:
                    success = False
        else:
            success = False
        
    return success, width, height, depth, name, xmin, ymin, xmax, ymax, classid

