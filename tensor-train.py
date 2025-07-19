#!./tensorflow/bin/python

import tensorflow as tf
import sys
from os import walk
import cv2
import numpy as np

print(tf.__version__)

# Import TensorFLow into your program to get started 
mnist = tf.keras.datasets.mnist

# Load the dataset, look in the 'Lables' directory and find the 
# DJI_0022.txt files and correlate them with the 
# DJI_0022.JPG files

TrainingSetPath="Labels"

textFileList = []
jpgFileList = [] 
for (dirpath, dirnames, filenames) in walk(TrainingSetPath):
    for filename in filenames:
        lastPeriod=filename.rfind('.')
        if lastPeriod > 0:
            if filename[lastPeriod:].lower() == ".txt":
                textFileList.append(filename)
            elif filename[lastPeriod:].lower() == ".jpg":
                jpgFileList.append(filename)

# xyFileList contains a dictionary, associating image file with text file 
xyFileList = []

for x in textFileList:
    xLastPeriod=x.rfind('.')
    for y in jpgFileList:
        yLastPeriod=y.rfind('.')
        if x[:xLastPeriod] == y[:yLastPeriod]:
            xyFileList.append({'image': y, 'text':x})


# Open each text file and get the first character before the first space and 
# put it in the y_train list 
y_train = [] 
maxNum = 0

# Fetch the first value from the input file 
for x in xyFileList: 
    number_str = ""
    with open(TrainingSetPath + "/" + x["text"]) as f:
        while True:
            c = f.read(1)
            if not c or c == ' ':
                break
            else:
                number_str = number_str + c
    number_int = int(number_str)
    x['y_train_index'] = number_int
    if number_int > maxNum:
        maxNum = number_int

# Set the index size for later on 
maxNum = maxNum + 1
imgHeight = 0
imgWidth = 0

# Use OpenCV NumPy interface, gotten from: 
# https://stackoverflow.com/questions/7762948/how-to-convert-an-rgb-image-to-numpy-array
for x in xyFileList:
    imageFilePath = TrainingSetPath + "/" + x["image"]
    print("Reading in: " + imageFilePath)
    im = cv2.imread(imageFilePath, cv2.COLOR_BGR2RGB) 
    
    if imgHeight == 0:
        imgHeight = np.size(im, 0)
        imgWidth = np.size(im, 1)
    elif np.size(im, 0) != imgHeight or imgWidth != np.size(im, 1):
        print("Error: Image height is not like the rest " + str(np.size(im, 0) + " != " + str(imgHeight) + " or " + str(np.size(im, 1)) + " != " + str(imgWidth)))
        sys.exit(1)
    
    x["x_train"] = im

# Create the y_train array, it is an array of arrays of floats, the size of 
# the second array is the number of different trees we're identifying. 
# Each index represents a probability of it being the designated tree in the 
# classes.txt file 
for x in xyFileList: 
    array = np.zeros(maxNum, dtype=float)
    array[x['y_train_index']] = 1.0
    x["y_train"] = array



x_train = np.empty([])
y_train = np.empty([])

# Populate the arrays 
for n in xyFileList:
    np.append(x_train, n["x_train"])
    np.append(y_train, n["y_train"])

print(str(x_train.ndim))

sys.exit(0)

# Build a machine learning model
# Sequential is useful for stacking layers where each layer has one input
# tensor and one output tensor. Layers are functions with a known mathmatical 
# structure that can be reused and have trainable variables. Most TensorFlow 
# models are composed of layers. This model uses the Flatten, Dense, and Dropout
# layers. 
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(imgHeight, imgWidth, 3)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

# For each example, the model returns a vector of logits or log-odds scores, 
# one for each class. 
predictions = model(x_train[:1]).numpy()
predictions

#The tf.nn.softmax function converts these logits to probabilities for each class:
tf.nn.softmax(predictions).numpy()

# Define a loss function for training using losses.SparseCategoricalCrossentropy:
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

#The loss function takes a vector of ground truth values and a vector of logits and returns a scalar loss for each example. This loss is equal to the negative log probability of the true class: The loss is zero if the model is sure of the correct class.

# This untrained model gives probabilities close to random (1/10 for each class), so the initial loss should be close to -tf.math.log(1/10) ~= 2.3.
loss_fn(y_train[:1], predictions).numpy()

# Before you start training, configure and compile the model using Keras Model.compile. Set the optimizer class to adam, set the loss to the loss_fn function you defined earlier, and specify a metric to be evaluated for the model by setting the metrics parameter to accuracy.
model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

     
# Use the Model.fit method to adjust your model parameters and minimize the loss:
model.fit(x_train, y_train, epochs=5)

# The Model.evaluate method checks the model's performance, usually on a validation set or test set.
# model.evaluate(x_test,  y_test, verbose=2)

# The image classifier is now trained to ~98% accuracy on this dataset. To learn more, read the TensorFlow tutorials.

# If you want your model to return a probability, you can wrap the trained model, and attach the softmax to it:
probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

#Congratulations! You have trained a machine learning model using a prebuilt dataset using the Keras API.

# For more examples of using Keras, check out the tutorials. To learn more about building models with Keras, read the guides. If you want learn more about loading and preparing data, see the tutorials on image data loading or CSV data loading.
probability_model(x_test[:5])


