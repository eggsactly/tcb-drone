#!./tensorflow/bin/python

import tensorflow as tf

print(tf.__version__)

# Import TensorFLow into your program to get started 
mnist = tf.keras.datasets.mnist

# Load the dataset
# Load and prepare the MNIST dataset. The pixel values of the images range from
# 0 through 255. Scale these values to a range of 0 to 1 by dividing the values
# by 255.0. This also converts the sample data from integers to floating-point
# numbers. 
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Build a machine learning model
# Sequential is useful for stacking layers where each layer has one input
# tensor and one output tensor. Layers are functions with a known mathmatical 
# structure that can be reused and have trainable variables. Most TensorFlow 
# models are composed of layers. This model uses the Flatten, Dense, and Dropout
# layers. 
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
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
model.evaluate(x_test,  y_test, verbose=2)

# The image classifier is now trained to ~98% accuracy on this dataset. To learn more, read the TensorFlow tutorials.

# If you want your model to return a probability, you can wrap the trained model, and attach the softmax to it:
probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

#Congratulations! You have trained a machine learning model using a prebuilt dataset using the Keras API.

# For more examples of using Keras, check out the tutorials. To learn more about building models with Keras, read the guides. If you want learn more about loading and preparing data, see the tutorials on image data loading or CSV data loading.
probability_model(x_test[:5])


