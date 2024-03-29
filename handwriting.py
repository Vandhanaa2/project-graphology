# -*- coding: utf-8 -*-
"""Copy of Handwriting2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dLyByAGBsWQp0lDsnXOUBz5MP1juF1Ks
"""

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn import preprocessing 
Standardisation = preprocessing.StandardScaler()

def show_image(image):
  print(plt.imshow(image))

def get_image(link):
    #import image
    image = cv2.imread(link)
    # image = image.astype('uint8')
    #plt.imshow(image)
    return image

def get_gray_scale(image):
  #grayscale  
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  return gray

def get_binary(gray):
  #binary
  ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
  return thresh

def do_dilation(thresh):
  #dilation
  kernel = np.ones((5,5), np.uint8)
  img_dilation = cv2.dilate(thresh, kernel, iterations=1)
  return img_dilation

def get_left_margin(thresh):
  ## Left Margin
  h, w = thresh.shape
  minval = h * w
  for i in range(h):
    cnt = 0
    for j in range(w):
      if thresh[i][j] == 0:
        cnt = cnt + 1
      else:
        break
    minval = min(minval, cnt)
  return minval

def get_right_margin(thresh):
  ## Right Margin
  h, w = thresh.shape
  minval = h * w
  i = 0
  while i < h:
    cnt = 0
    j = 0
    while j < w:
      if thresh[i][j] == 0:
        cnt = cnt + 1
        j = j + 1
      else:
        break
    minval = min(minval, cnt)
    i = i + 1
  return minval

def get_pen_pressure(gray):
  h, w = gray.shape
  cnt = 0
  sum = 0
  for i in range(h):
    for j in range(w):
      if gray[i][j] > 0:
        cnt = cnt + 1
        sum = sum + gray[i][j]
  val = sum/cnt
  return val

def get_slant_document(thresh):
  # grab the (x, y) coordinates of all pixel values that
  # are greater than zero, then use these coordinates to
  # compute a rotated bounding box that contains all
  # coordinates
  coords = np.column_stack(np.where(thresh > 0))
  angle = cv2.minAreaRect(coords)[-1]

  # the `cv2.minAreaRect` function returns values in the
  # range [-90, 0); as the rectangle rotates clockwise the
  # returned angle trends to 0 -- in this special case we
  # need to add 90 degrees to the angle
  if angle < -45:
    angle = -(90 + angle)

  # otherwise, just take the inverse of the angle to make
  # it positive
  else:
    angle = -angle
  return angle

def get_slant_words(dilation):
  #find contours
  #im2,ctrs, hier = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  img, ctrs, hier = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
  #sort contours
  sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
 
  sum_of_angles = 0
  num_words = 0
  for i, ctr in enumerate(sorted_ctrs):
    angle = cv2.minAreaRect(ctr)[-1]

    if angle < -45:
      angle = -(90 + angle)

    else:
      angle = -angle
    num_words += 1
    sum_of_angles += angle
  if num_words != 0:
    return (sum_of_angles / num_words)
  else:
    return 0

def get_space_lines(thresh):
  h, w = thresh.shape
  spaces = []
  for i in range(h):
    cnt = 0
    for j in range(w):
      if thresh[i][j] > 0:
        cnt += 1
    if cnt == 0:
      spaces.append(1)
    else: 
      spaces.append(0)
  continous_lines = []
  cnt = 0
  for i in spaces:
    if i == 1:
      cnt = cnt + 1
    else:
      if cnt != 0:
        continous_lines.append(cnt)
      cnt = 0
  length = len(continous_lines)
  minval = h * w
  for i in range(length):
    if i == 0:
      continue
    else:
      minval = min(minval, continous_lines[i])
  return minval

def get_all_parameters(link):
  param = []
  
  # Get the image from the link
  image = get_image(link)
  image = image.astype('uint8')
  # plt.imshow(image)
  
  # Convert the image to gray image
  gray  = get_gray_scale(image)
  # plt.imshow(gray)
  
  # Convert the gray scale image to Binary image
  thresh = get_binary(gray)
  # plt.imshow(thresh)

  # Perform Dilation
  dilation = do_dilation(thresh)
  # plt.imshow(dilation)
  
  ##  Calculate left margin
  left_margin  = get_left_margin(thresh)
  param.append(left_margin)
  
  # Calcualte right margin
  right_margin = get_right_margin(thresh)
  param.append(right_margin)
  
  # Calculate space lines
  space_lines  = get_space_lines(thresh)
  param.append(space_lines)
  
  # Calculate the pen pressure
  pen_pressure = get_pen_pressure(gray)
  param.append(pen_pressure)
  
  # Calculate the slant of the document
  slant_document = get_slant_document(thresh)
  param.append(slant_document)
  
  # Calculate slant of the words
  slant_words = get_slant_words(thresh)
  param.append(slant_words)
  
  return param

# def build_Xtrain():
#   X_train = []
#   i = 0
#   for i in range(1,31):
#     if i == 43 or i == 44 or i == 45 :
#       continue
#     path = "./drive/My Drive/FAMDATASAMPLE/" + str(i) + ".jpg"
#     param = get_all_parameters(path)
#     print(path)
#     X_train.append(param)
#   return X_train

# X_train = build_Xtrain()

# X_train

# ## To Get Y_train
# df = pd.read_excel ('./Y_train.xlsx')
# print (df)

labels = ['Introvert','Extrovert','Adaptive','Reserved','Social','Practical','Emotional','Ignorant','Optimistic','Confident','Pessimistic','Egoistic','Selfless']

# # Ytrain of size 30 with each entry have 13 size numpy array for labels
# Y_train = []
# for i in range(30):
#   arr = np.linspace(0, 0, 13)
#   Y_train.append(arr)

# k = 0
# for i in range(30):
#     j = 3
#     for k in range(13):
#       Y_train[i][k] = df.iloc[i,j]
#       j += 1
#       if j == 16:
#         break

# k=0
# for i in range(30):
#   for k in range(13):
#       print(Y_train[i][k],end=" ")
#   print()

from sklearn.linear_model import LogisticRegression

# X_temp = X_train[:2]
# print(X_temp)

# X_train_temp = np.array(X_train)
# print(type(X_train_temp))

# models = []
# for lab in range(13):
#   Y_train_helper = []
#   for row in range(25):
#     Y_train_helper.append(Y_train[row][lab])
#   # all parameters not specified are set to their defaults
#   lr = LogisticRegression()
#   X_train_temp = np.array(X_train[:25])
#   #X_train_temp = Standardisation.fit_transform(X_train_temp)
#   Y_train_helper = np.array(Y_train_helper)
#   #print(X_train_temp.shape)
#   lr.fit(X_train_temp, Y_train_helper)
#   models.append(lr)

import pickle
# # # save the model to disk
# pickle.dump(models, open("/content/drive/My Drive/Models.pickle", 'wb'))
# !touch /drive/My Drive/Models.pickle
import os
# print(os.getcwd())
# path = "./static/images/Capture.JPG"
# image = cv2.imread(path)
# print(image)
# print(plt.imshow(image))
# image = image.astype('uint8')

# # Convert the image to gray image
# gray  = get_gray_scale(image)
# print(plt.imshow(gray))

# # Convert the gray scale image to Binary image
# thresh = get_binary(gray)
# print(plt.imshow(thresh))

# Perform Dilation
# dilation = do_dilation(thresh)
# print(plt.imshow(dilation))

##UnPickling the Model

pickle_Model = pickle.load(open("./Models.pickle", 'rb'))

def predict(link):
  predictions=[]
  XX = []
  X = get_all_parameters(link)
  XX.append(X)
  #XX = Standardisation.fit_transform(XX)
  XX = np.array(XX)
  for j in range(13):
    pred = pickle_Model[j].predict(np.array(XX))[0]
    if int(pred) == 1:
         predictions.append(labels[j])
  return predictions 

#find contours
# im2,ctrs, hier = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#sort contours
# sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

# for i, ctr in enumerate(sorted_ctrs):
#     # Get bounding box
#     x, y, w, h = cv2.boundingRect(ctr)
#     print(x,y)

#     # Getting ROI
#     roi = image[y:y+h, x:x+w]

#     # show ROI
#     #plt.imshow(roi)
#     cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
# plt.imshow(image)

# predict("./drive/My Drive/sample_img.jpg")

