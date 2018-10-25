#!/usr/bin/env python
# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from shapedetector import ShapeDetector
#import argparse
import numpy as np
import imutils
import cv2


# load the image and background
image = cv2.imread("game.png")
bg = cv2.imread("board.png")

# Apply same process to the background
resized_bg = imutils.resize(bg, width=300)
ratio_bg = bg.shape[0] / float(resized_bg.shape[0])

gray_bg = cv2.cvtColor(resized_bg, cv2.COLOR_BGR2GRAY)
blurred_bg = cv2.GaussianBlur(gray_bg, (5, 5), 0)
thresh_bg = cv2.threshold(blurred_bg, 60, 255, cv2.THRESH_BINARY)[1]
#swap color
thresh_bg = ~thresh_bg

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
thresh_result = thresh - thresh_bg

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
	#print(cX)
	#print(cY)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)

	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)
#cv2.imshow("Image", image)
#cv2.waitKey(0)
cv2.destroyAllWindows()