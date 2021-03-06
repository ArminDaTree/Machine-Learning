# -*- coding: utf-8 -*-
"""Pneumonia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1euaRHib-YWVUF4BBbFDeLLQDUT5s7UMh
"""

!pip install -q kaggle
 from google.colab import files 
 files.upload() #put kaggle.json API
!mkdir ~/.kaggle 
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!kaggle datasets download -d paultimothymooney/chest-xray-pneumonia #download at .zip
#unzipping the zip files and deleting the zip files
!unzip \*.zip  && rm *.zip

#imports
from time import time
import tensorflow as tf
import numpy as np
import os
from tensorflow import keras
from tensorflow.keras import datasets, layers, models, losses
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, Flatten, MaxPool2D, Dense, Dropout , BatchNormalization
import matplotlib.pyplot as plt
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.python.keras.applications.vgg16 import preprocess_input #preprocess FOR VGG16
from keras.callbacks import EarlyStopping,ModelCheckpoint

train_datagen = ImageDataGenerator(zoom_range=0.15,width_shift_range=0.2,height_shift_range=0.2,shear_range=0.15)
test_datagen = ImageDataGenerator()
train_generator = train_datagen.flow_from_directory('./chest_xray/chest_xray/train',target_size=(224, 224),batch_size=32,shuffle=True,class_mode='binary')
test_generator = test_datagen.flow_from_directory('./chest_xray/chest_xray/test',target_size=(224,224),batch_size=32,shuffle=False,class_mode='binary')

"""# Utilisation du modèle VGG16"""

#VGG 16
model = keras.models.Sequential()

model.add(Conv2D(input_shape=(224,224,3), kernel_size=(3,3),filters=64,padding="same", activation="relu"))
model.add(Conv2D(kernel_size=(3,3), filters=64, padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2))) #move 2 pixels by 2 pixels

model.add(Conv2D(kernel_size=(3,3), filters=128, padding="same", activation="relu"))
model.add(Conv2D(kernel_size=(3,3), filters=128, padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Conv2D(kernel_size=(3,3), filters=256, padding="same", activation="relu"))
model.add(Conv2D(kernel_size=(3,3), filters=256, padding="same", activation="relu"))
model.add(Conv2D(kernel_size=(3,3), filters=256, padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Conv2D(kernel_size=(3,3), filters=512, padding="same", activation="relu"))
model.add(Conv2D(kernel_size=(3,3), filters=512, padding="same", activation="relu"))
model.add(Conv2D(kernel_size=(3,3), filters=512, padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))


model.add(Flatten())
model.add(Dense(4096, activation="relu"))
model.add(Dense(4096, activation="relu"))
model.add(Dense(2, activation="softmax"))
opt = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt, loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=["accuracy"])
model.summary()

from keras_preprocessing import image
images = image.load_img("/content/chest_xray/chest_xray/val/NORMAL/NORMAL2-IM-1437-0001.jpeg", target_size=(224,224,3))    
x = image.img_to_array(images)
plt.imshow(x.astype('uint8'))
x = np.expand_dims(x, axis=0) 
print(x.shape)
model_outpout = model.predict(x)
print(model_outpout)

history = model.fit(train_generator,validation_data=test_generator,epochs=5)
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch') 
plt.ylabel('Accuracy')
plt.ylim([0.8, 1])
plt.legend(loc='lower right')
plt.show()



"""# Tentative de modèle"""

#first try model
model2 = keras.models.Sequential()
#stride = 1 : we move 1 pixel by 1 for conv
model2.add(Conv2D(128, (3,3), strides=(1,1), activation="relu", input_shape=(128,128,3), padding="same"))
model2.add(MaxPool2D(2))

model2.add(Conv2D(64, (3,3), strides=(1,1), activation="relu", padding="same"))
model2.add(MaxPool2D(2))

model2.add(Conv2D(32, (3,3), strides=(1,1), activation="relu", padding="same"))
model2.add(MaxPool2D(2))

model2.add(Conv2D(16, (3,3), strides=(1,1), activation="relu", padding="same"))
model2.add(MaxPool2D(2))
#fully connected layers
model2.add(Flatten())
model2.add(Dense(32, activation="relu"))
model2.add(Dense(2, activation="softmax"))

model2.compile(optimizer="adam", loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=["accuracy"])
model2.summary()

IMGSIZE = 128

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,#random rotation
        zoom_range=0.2, #random zoom
        horizontal_flip=True)#Randomly flip inputs horizontally
test_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
        './chest_xray/chest_xray/train',
        target_size=(IMGSIZE, IMGSIZE),
        class_mode='binary')
validation_generator = test_datagen.flow_from_directory(
        './chest_xray/chest_xray/test',
        target_size=(IMGSIZE, IMGSIZE),
        class_mode='binary')
print(train_generator.image_shape)
print(train_generator.class_indices )

history = model2.fit(train_generator,validation_data=validation_generator,epochs=5)
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch') 
plt.ylabel('Accuracy')
plt.ylim([0.8, 1])
plt.legend(loc='lower right')
plt.show()

scores = model2.evaluate(validation_generator)
print("Loss of the model: %.2f"%(scores[0]))
print("Test Accuracy: %.2f%%"%(scores[1] * 100))

from keras_preprocessing import image
images = image.load_img("/content/chest_xray/chest_xray/val/PNEUMONIA/person1950_bacteria_4881.jpeg", target_size=(128,128,3))    
x = image.img_to_array(images)
plt.imshow(x.astype('uint8'))
x = np.expand_dims(x, axis=0)
x = x/255.0
print(x.shape)
model_outpout = model2.predict(x)
print(model_outpout)
if model_outpout[0,0] > model_outpout[0,1]:
  val = "normal"
  max = 0
else:
  val = "malade (pneumonie)"
  max = 1
#print(model_outpout)
#print(x.shape)
print("Le modèle prédit que le patient est ", val, "avec une probabilité de ", str(model_outpout[0, max]*100)[:5], "%")