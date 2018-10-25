#!/usr/bin/env python

# import the necessary packages
from shapedetector import ShapeDetector
#import argparse
import numpy as np
import imutils
import cv2

def line_intersection(line1, line2):
	xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
	ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

	def det(a,b):
		return a[0] * b[1] - a[1] * b[0]
	
	div = det(xdiff, ydiff)
	if div == 0:
		raise Exception('Lines do not intersect')
	d = (det(*line1), det(*line2))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div

	return x, y

def Get_Intersection(bg):

	#gray = cv2.cvtColor(bg,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(bg,50,150,apertureSize = 3)
	lines = cv2.HoughLines(edges,1,np.pi/180,200)
	line_points = []

	for line in lines:
		for rho,theta in line:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))
			
			line_points.append(((x1,y1),(x2,y2)))
			cv2.line(bg,(x1,y1),(x2,y2),(0,0,255),2)

	A = line_intersection(line_points[0], line_points[2])
	B = line_intersection(line_points[1], line_points[2])
	C = line_intersection(line_points[0], line_points[3])

	return A,B,C

def Locate_position(X,Y,inter):
	A = inter[0];
	B = inter[1];
	C = inter[2];

	if X < A[0]:
		if Y < A[1]:
			return 1
		elif Y > C[1]:
			return 7
		else:
			return 4
	elif X > B[0]:
		if Y < A[1]:
			return 3
		elif Y > C[1]:
			return 9
		else:
			return 6
	else:
		if Y < A[1]:
			return 2
		elif Y > C[1]:
			return 8
		else:
			return 5

# load the image and background
image = cv2.imread("game.png")
bg = cv2.imread("board.png")

# Apply same process to the background
resized_bg = imutils.resize(bg, width=300)
ratio_bg = bg.shape[0] / float(resized_bg.shape[0])
gray_bg = cv2.cvtColor(resized_bg, cv2.COLOR_BGR2GRAY)
#blurred_bg = cv2.GaussianBlur(gray_bg, (5, 5), 0)
#thresh_bg = cv2.threshold(blurred_bg, 60, 255, cv2.THRESH_BINARY)[1]
#swap color
gray_bg = ~gray_bg
inter = Get_Intersection(gray_bg)
print (inter)

# resize it to a smaller factor so that
# the shapes can be approximated better
#convert the resized image to grayscale, blur it slightly,
# and threshold it
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
#swap color
thresh = ~thresh

#result image
#thresh_result = thresh - gray_bg
thresh_result = thresh

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh_result.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)

	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)
	lo = Locate_position(cX, cY, inter)
	#print(cX,cY)
	print(lo)
	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)
#cv2.imshow("Image", image)
#cv2.waitKey(0)
cv2.destroyAllWindows()