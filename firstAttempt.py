#!./tensorflow/bin/python

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator


print(tf.__version__)

class_labels = ['Ironwood', 'Mesquite', 'PaloVerde']
train_path = 'Data/'
train_batches = ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input).flow_from_directory(directory=train_path,target_size=(224,224), classes=class_labels, batch_size=6)

test_batch = ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input).flow_from_directory(directory=train_path,target_size=(224,224), classes=['test'])

# Build a machine learning model
# Sequential is useful for stacking layers where each layer has one input
# tensor and one output tensor. Layers are functions with a known mathmatical 
# structure that can be reused and have trainable variables. Most TensorFlow 
# models are composed of layers. This model uses the Flatten, Dense, and Dropout
# layers. 
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(224, 224, 3)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(3)
])

print(model.summary())


# Before you start training, configure and compile the model using Keras Model.compile. Set the optimizer class to adam, set the loss to the loss_fn function you defined earlier, and specify a metric to be evaluated for the model by setting the metrics parameter to accuracy.
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Use the Model.fit method to adjust your model parameters and minimize the loss:
model.fit(x=train_batches, epochs=2, verbose=2)

# The Model.evaluate method checks the model's performance, usually on a validation set or test set.
#model.evaluate(x_test,  y_test, verbose=2)

# If you want your model to return a probability, you can wrap the trained model, and attach the softmax to it:
probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

raw_predict = model.predict(test_batch)
print(raw_predict)

predictions = probability_model.predict(test_batch)
print(predictions)

print(class_labels)
