import os

import cv2

listF = os.listdir('dir_znaky')
filImage = 'pvi_cv07_people.jpg'
bgr = cv2.imread(filImage)
gray = cv2.cvtColor(bgr, cv2.COLOR_RGB2GRAY)
boxes = []
with open('pvi_cv07_boxes_01.txt') as f:
    lines = f.read().splitlines()
for line in lines:
    vec = line.split(' ')
    vec = [int(x) for x in vec]
    boxes.append(vec)
for (x, y, w, h) in boxes:
    cv2.rectangle(bgr, (x, y), (x + w, y + h), (0, 0, 255), 2)
    faceCascade = cv2.CascadeClassifier(
    'pvi_cv07_haarcascade_frontalface_default.xml') # Detect faces in the

#image
faces = faceCascade.detectMultiScale(gray,
scaleFactor=1.4,
minNeighbors=5,
minSize=(30, 30),
flags=cv2.CASCADE_SCALE_IMAGE)