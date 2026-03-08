#!./tensorflow/bin/python

import tensorflow as tf
import sys
from os import walk
import cv2
import numpy as np
from libs.parse_annotation import *

PROGRAM_NAME=str(sys.argv[0].lstrip('.').lstrip('/'))

print(tf.__version__)

TrainingSetPathList=[
      "RillitoPark"
    , "CherryAvePark"
]

trainImageHeight=500
trainImageWidth=500

# classesArray is a list of trees
classesArray = []

## 1. Produce list of files 
# Parse the tagged files 
textFileList = []
jpgFileList = [] 
for TrainingSetPath in TrainingSetPathList:
    for (dirpath, dirnames, filenames) in walk(TrainingSetPath):
        for filename in filenames:
            lastPeriod=filename.rfind('.')
            if lastPeriod > 0:
                if filename[lastPeriod:].lower() == ".xml":
                    textFileList.append(TrainingSetPath + "/" + filename)
                elif filename[lastPeriod:].lower() == ".jpg":
                    jpgFileList.append(TrainingSetPath + "/" + filename)
                else:
                    print(PROGRAM_NAME + ": Warning: Unidentified extension: " + str(filename[lastPeriod:]) + " found on file path, " + str(filename) + ", continuing.", file=sys.stderr)
    
#print(str(textFileList))
#print(str(jpgFileList))
#sys.exit()    
   
# xyFileList contains a dictionary, associating image file with text file 
xyFileList = []
# Open each text file and get the first character before the first space and 
# put it in the y_train list 
y_train = [] 
x_train = []
maxNum = 0

## 2. Associate images with xml files 
# For each text file, associate xml with the associated image 
for x in textFileList:
    xLastPeriod=x.rfind('.')
    for y in jpgFileList:
        yLastPeriod=y.rfind('.')
        if x[:xLastPeriod] == y[:yLastPeriod]:
            xyFileList.append({'image': y, 'text':x, 'parsed': False})

# treeList holds a dictionary of the parameters
# 'xmin': x coordinate of upper left corner of bounding box
# 'ymin': y coordinate of upper left corner of bounding box
# 'xmax': x coordinate of lower right corner of bounding box
# 'ymax': y coordinate of lower right corner of bounding box
# 'treeID': index of tree type stored in classesArray
# 'imageID':  index of image stored in xyFileList

treeList = []

## 3. Parse XML
# Fetch the first value from the input file,
# x is a dictionary of 'image' and 'text'
# This loop parses the input files 
imageCounter = -1
for x in xyFileList: 
    imageCounter = imageCounter + 1
    xLastPeriod=x["text"].rfind('.')  
    parseList = []
    # When the tag file associated with the image is an xml file
    if x["text"][xLastPeriod:] == '.xml':
        success, width, height, depth, parseList = parseDronePicsXml(x["text"], classesArray)
        if not success:
            print(PROGRAM_NAME + ": Warning: Issue parsing: " + str(x["text"]) + " for " + str(x["image"]) + " skipping", file=sys.stderr)
            continue
    else:
        print(PROGRAM_NAME + ": Warning: No parser for extension: " + str(x["text"][xLastPeriod:]) + " for " + str(x["image"]) + " skipping", file=sys.stderr)
        continue
    #x['y_train_index'] = number_int
    
    for i in parseList:
        treeList.append({'xmin': i['xmin'], 'ymin': i['ymin'], 'xmax': i['xmax'], 'ymax': i['ymax'], 'treeID': i['classID'], 'imageID': imageCounter})
    x['parsed'] = True
                    

numTrees=len(treeList)
numTreeTypes=len(classesArray)

# x_train contains the list of images it is aligned with y_train, which is the
# list of arrays of indicies into class array. 
x_train = np.zeros(shape=(numTrees, trainImageHeight, trainImageWidth, 3), dtype=np.uint8)
y_train = np.zeros(shape=(numTrees, numTreeTypes))
## 4. Produce cropped images and put into x_train, which is the list of images
imageCounter = 0
for i in treeList:
    im = cv2.imread(xyFileList[i['imageID']]['image'], cv2.COLOR_BGR2RGB) 
    cropped_image = im[i['ymin']:i['ymax'], i['xmin']:i['xmax']] 
    resized_image = cv2.resize(cropped_image, (trainImageHeight, trainImageWidth)) 
    x_train[imageCounter] = resized_image
    a = [0.0] * len(classesArray)
    y_train[imageCounter][i['treeID']] = 1.0
    imageCounter = imageCounter + 1
    

           
