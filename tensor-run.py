#!./tensorflow/bin/python

import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout, MaxPooling2D, BatchNormalization
from tensorflow.keras.models import Model, load_model
import sys
from os import walk
import cv2
import numpy as np

TrainingSetPath="Labels"
indexRecord="classes.txt"

resize_width=1000
resize_height=562
maxNum = 3
checkpoint_path = "TreeIdentifyTensorFlowModel.keras"

def get_model():
    # Create a simple model.
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(resize_height, resize_width, 3)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(maxNum)
    ])
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])
    return model


print(tf.__version__)

classesArray = []

if len(sys.argv) < 2:
    print (sys.argv[0] + ": error: positional input parameter 1 should be the path to an image.")
    sys.exit(1)

inputImage = sys.argv[1]

# Read in the classes file, which contains a record of the trees we trained on
file_path = TrainingSetPath + "/" + indexRecord
try:
    with open(file_path, 'r') as file:
        for line in file:
            # Each 'line' variable will contain one line from the file,
            # including the newline character at the end (e.g., '\n').
            # You can process each line here.
            classesArray.append(line.strip())  # .strip() removes leading/trailing whitespace, including newlines
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

# Load in the image from inputs from stdin 
im = cv2.imread(inputImage, cv2.COLOR_BGR2RGB) 

# We want to set the input image to the size of the images the network was 
# trained on 
dsize=(resize_width, resize_height)
im = cv2.resize(im, dsize) 

print("It takes a long time to load the model...")

model = tf.keras.models.load_model(checkpoint_path)
if model is not None:
    print(sys.argv[0] + ": info: Model loaded successfully!")
else:
    print(sys.argv[0] + ": error: Failed to load the model.")
    sys.exit(1)

image_in_array = np.vstack([[im]])

# Evaluate the model
result = model.predict(image_in_array[:1])
print("Result: " + str(result))

index=0
indexOfHighestValue=-1
highestValue=0
# find index of the greatest value
for probability in result[0]:
    if probability > highestValue:
        indexOfHighestValue = index
    index = index + 1

if indexOfHighestValue >= 0:
    print("\"" + classesArray[indexOfHighestValue] + "\" identified")
else:
    print("Could not identify tree")

