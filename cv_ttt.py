#!/usr/bin/env python

# import the necessary packages
import cv2
import numpy


class boardMap():
	def __init__(self,img,A,B,C,D):
		self.A = A
		self.B = B
		self.C = C
		self.D = D
		self.savedImage = img

	def updateSavedImage(self,img):
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
		lower = numpy.array([30,0,0],numpy.uint8)
		upper = numpy.array([179,100,80],numpy.uint8)
		
		lowerH = numpy.array([0,20,0],numpy.uint8)
		upperH = numpy.array([30,255,255],numpy.uint8)
		
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		
		# check for hand
		maskH = cv2.inRange(hsv, lowerH, upperH)
		_, cntH, heirarchy = cv2.findContours(maskH[:], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contourLengthH  = len(cntH)
		if contourLengthH > 0:
			for i in range(contourLengthH):
				if cv2.contourArea(cntH[i]) > 500:
					return 0
					#pass
		
		# find difference
		mask = cv2.inRange(hsv, lower, upper)
		
		hsv2 = cv2.cvtColor(self.savedImage, cv2.COLOR_BGR2HSV)
		mask2 = cv2.inRange(hsv2, lower, upper)
		
		fgmask = mask - mask2
		
		# dilate and erode
		fgmask2 = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, numpy.ones((5,5)))
		# dilate
		#fgmask3 = cv2.dilate(fgmask, numpy.ones((11,11)))
		
		# find contours in the thresholded image
		_, cnts, heirarchy = cv2.findContours(fgmask2[:], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		#cv2.imshow("Mask", maskH)
		#cv2.waitKey(0)
		
		contourLength  = len(cnts)
		# Check for at least one target found
		if contourLength < 1:
			return 0
			print("No target found")

		# target found
		## Loop through all of the contours, and get their areas
		area = [0.0]*contourLength
		for i in range(contourLength):
			a = cv2.contourArea(cnts[i])
			if a > 40:
				area[i] = a 

		#### Target #### the largest object
		maxA = max(area)
		#print(maxA)
		if maxA < 1:
			return 0
		c = cnts[area.index(maxA)]
		#print(max(area))
		# show the output image
		cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
		cv2.imshow("Image", img)
		cv2.waitKey(0)
		#if cv2.waitKey(1) & 0xFF == ord('q'):
		#	pass

		# compute the center of the contour
		M = cv2.moments(c)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		#print(cX,cY)
		
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
