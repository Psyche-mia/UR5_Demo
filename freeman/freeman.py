# -*- coding: utf-8 -*-
import cv2

import numpy as np

import pandas as pd

img = cv2.imread('bird.jpg')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret, binary =cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

binary,contours, hierarchy =cv2.findContours(binary,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cv2.drawContours(img,contours,-1,(0,0,255),3)

cv2.imshow("img", img)

cv2.waitKey(0)

#cv2.RETR_TREE
img2 = cv2.imread('blank.png')

cv2.drawContours(img2,contours[1],-1,(0,0,255),1)

cv2.imshow("img2", img2)

cv2.waitKey(0)

print (type(contours))

print (type(contours[0]))

print (len(contours[0]))

print (contours[1][0][0][0])

#print (contours[0]-contours[0])

columns = []

for i in range(1480):

	columns.append(contours[1][i]-contours[1][i - 1])

#print (len(columns))

#print (columns[1][0][0])

a = []

for i in range(1480):

	if columns[i][0][0] == 0 and columns[i][0][1] ==-1:

		a.append(6)

	elif columns[i][0][0] == 0 and columns[i][0][1] ==1:

		a.append(2)

	elif columns[i][0][0] == 1 and columns[i][0][1] ==1:

		a.append(1)

	elif columns[i][0][0] == 1 and columns[i][0][1] ==0:

		a.append(0)

	elif columns[i][0][0] == 1 and columns[i][0][1] ==-1:

		a.append(7)

	elif columns[i][0][0] == -1 and columns[i][0][1] ==1:

		a.append(3)

	elif columns[i][0][0] == -1 and columns[i][0][1] ==0:

		a.append(4)

	elif columns[i][0][0] == -1 and columns[i][0][1] ==-1:

		a.append(5)

#print(a)

#f= open("freemancode.txt","w+")
#for i in a:
#     f.write("%d\r\n " % a(i))
#f.close()
