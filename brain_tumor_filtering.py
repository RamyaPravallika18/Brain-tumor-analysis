# -*- coding: utf-8 -*-
"""Brain tumor filtering.ipynb
"""

from google.colab import files

"""After importing we are uploading the dataset we have"""

uploaded=files.upload()

"""unzipping the dataset"""

!unzip brain_tumor_dataset.zip
!rm brain_tumor_dataset.zip

"""Assigning batch size for training the data"""

batch_size=9

"""Importing all the libraries """

import pandas as pd
import cv2
import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import tensorflow as tf
from tensorflow import keras

"""Training the data"""

directory='brain_tumor_dataset'
train_datagen= ImageDataGenerator(validation_split=0.2,
                                  rescale=1./255,
                                  rotation_range=40,
                                  width_shift_range=0.2,
                                  height_shift_range=0.2,
                                  zoom_range=0.2,
                                  horizontal_flip=True,
                                  fill_mode='nearest')
train_generator= train_datagen.flow_from_directory(
                                  directory,
                                  target_size = (70, 70),
                                  batch_size = batch_size,
                                  class_mode ='binary',
                                  seed=2020,
                                  subset = 'training')

"""Plotting the trained dataset images 
Tumor exist=1
Tumor won't exist=0
"""

imgs, labels = next(train_generator)
def plotimages(images_arr):
  fig, axes = plt.subplots(1, batch_size, figsize=(20,20))
  axes = axes.flatten()
  for img, ax in zip( images_arr, axes):
    ax.imshow(img)
    ax.axis('off')
  plt.tight_layout()
  plt.show()
plotimages(imgs);
print(labels);

"""Adding 30% of noise to the images """

import cv2
import numpy as np
from skimage.util import random_noise
i1 = cv2.imread("/content/brain_tumor_dataset/yes/Y1.jpg")
noise_i1 = random_noise(i1, mode='s&p',amount=0.3)
noise_i1 = np.array(255*noise_i1, dtype = 'uint8')
plt.imshow(noise_i1)
cv2.waitKey(0)

"""Median filter algorithm"""

dst1 = cv2.medianBlur(i1,7)

"""Plotting the median filter image and the original image"""

plt.figure(figsize=(11,6))
plt.subplot(121), plt.imshow(noise_i1),plt.title('Salt&pepperNoise')
plt.subplot(122), plt.imshow(cv2.cvtColor(dst1, cv2.COLOR_HSV2RGB)),plt.title('Median filter')
plt.show()

"""Mean filter algorithm & 
Plotting both mean filter image and the original image
"""

figure_size = 9 
new_image1 = cv2.blur(i1,(figure_size, figure_size))
plt.figure(figsize=(11,6))
plt.subplot(121), plt.imshow(noise_i1),plt.title('Original')
plt.subplot(122), plt.imshow(cv2.cvtColor(new_image1, cv2.COLOR_HSV2RGB)),plt.title('Mean filter')
plt.show()

"""Calculating the PSNR of each sample in a dataset"""

from math import log10, sqrt 
import cv2 
import numpy as np
import argparse
def PSNR(original, compressed):
 mse = np.mean((original - compressed) ** 2)
 print("\nMean square error(MSE) value is",mse)
 if(mse == 0):
  return 100
 max_pixel = 255.0
 psnr = 20 * log10(max_pixel / sqrt(mse))
 return psnr
def main():
  original =noise_i1
  compressed =new_image1
  ho, wo, _ = original.shape
  hc, wc, _ = compressed.shape
  ratio_orig = ho/wo
  ratio_comp = hc/wc
  dim = (wc, hc)
  if ho > hc and wo > wc:
    print("\nResizing original image for analysis")
    original = cv2.resize(original, dim)
  value = PSNR(original, compressed)
  print("\nPeak Signal-to-Noise Ratio (PSNR) value is", value, "dB")

if __name__ == '__main__':
	main()
