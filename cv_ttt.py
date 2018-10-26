#!/usr/bin/env python

# import the necessary packages
import cv2
import numpy as np


class boardMap():
	def __init__(self,img,A,B,C,D):
		self.A = A
		self.B = B
		self.C = C
		self.D = D
		self.savedImage = img

	def updateSavedImage(img):
		self.savedImage = img

	def getUserPosition(self,img):
		Ax = self.A[0]
		Ay = self.A[1]
		Bx = self.B[0]
		By = self.B[1]
		Cx = self.C[0]
		Cy = self.C[1]
		Dx = self.D[0]
		Dy = self.D[1]

		# Apply the background image to mask the image
		fgmask = img - self.savedImage()

		# convert the resized image to grayscale, blur it slightly, and threshold it
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

		# erode and dilate
		cv2.morphologyEx(thresh, cv2.MORPH_OPEN, numpy.ones((5,5)))
		# find contours in the thresholded image
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		contourLength  = len(cnts)
		# Check for at least one target found
		if contourLength < 1:
			return 0
			#print("No target found")

		# target found
		## Loop through all of the contours, and get their areas
		area = [0.0]*contourLength
		for i in range(contourLength):
			area[i] = cv2.contourArea(cnts[i])

		#### Target #### the largest object
		c = cnts[area.index(max(area))]
		# show the output image
		#cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)
		#cv2.imshow("Image", img)
		# compute the center of the contour
		M = cv2.moments(c)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		
		if cY < Ay:
			if cX < Ax:
				return 1
			elif cX < Bx:
				return 2
			else:
				return 3
		elif cY < Cy:
			if cX < Ax:
				return 4
			elif cX < Bx:
				return 5
			else:
				return 6
		else:
			if cX < Ax:
				return 7
			elif cX < Bx:
				return 8
			else:
				return 9


		#cv2.waitKey(0)

#cv2.imshow("Image", image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
