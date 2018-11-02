#!/usr/bin/env python

# import the necessary packages
import cv2
import numpy


class camera():
	def __init__(self,index):
		self.cap = cv2.VideoCapture(index)

	def updateSavedImage(self, img):
		self.savedImage = img
		
	def setABCD(self):
		while(True):
			# Capture frame-by-frame
			ret, image = cap.read()
			hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	
			#find lines in the image
			lower = numpy.array([30,0,0],numpy.uint8)
			upper = numpy.array([179,100,80],numpy.uint8)
			mask = cv2.inRange(hsv, lower, upper)

			# dilate and erode
			cv2.morphologyEx(mask, cv2.MORPH_CLOSE, numpy.ones((26,26))) 
			# erode and dilate
			cv2.morphologyEx(mask, cv2.MORPH_OPEN, numpy.ones((5,5)))
	
			# find lines
			lines = cv2.HoughLines(mask,1,3*numpy.pi/180, 250)
	
			if lines==None:
				cv2.imshow('frame',image)
				continue
		
			if len(lines) < 4:
				continue
		
			#Find (A,B),(C,D)
			rhoV = 0
			rhoH = 0
			for line in lines:
				rho,theta = line[0]
				a = numpy.cos(theta)
				b = numpy.sin(theta)
				x0 = a*rho
				y0 = b*rho
				x1 = int(x0 + 1000*(-b))
				y1 = int(y0 + 1000*(a))
				x2 = int(x0 - 1000*(-b))
				y2 = int(y0 - 1000*(a))
		
				cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
		
				# Horizontal
				if theta <= 3*numpy.pi/4 and theta > numpy.pi/4:
					if rhoH == 0:
						rhoH = rho
						lineH = ((x1,y1),(x2,y2))
					elif rho < rhoH-20:
						line0 = ((x1,y1),(x2,y2))
						line3 = lineH
					elif rho > rhoH+20:
						line3 = ((x1,y1),(x2,y2))
						line0 = lineH
				# Vertical
				else:
					if rhoV == 0:
						rhoV = rho
						lineV = ((x1,y1),(x2,y2))
					elif rho < rhoV-20:
						line1 = ((x1,y1),(x2,y2))
						line2 = lineV
					elif rho > rhoV+20:
						line2 = ((x1,y1),(x2,y2))
						line1 = lineV
	
			# Display the resulting frame
			cv2.imshow('frame',image)
		
			try:
				self.A = line_intersection(line0, line1)
				self.B = line_intersection(line0, line2)
				C = line_intersection(line1, line3)
				D = line_intersection(line2, line3)
				#print(A,B,C,D)
				
				for i in range(4):
					self.cap.grab()
				ret, image2 = cap.read()
				cv2.imshow('frame2',image2)
		
				bm = cv_ttt.boardMap(image2,A,B,C,D)
		
			except Exception as e:
				import traceback
				traceback.print_exc()
				print(e)

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
		
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower, upper)
		
		hsv2 = cv2.cvtColor(self.savedImage, cv2.COLOR_BGR2HSV)
		mask2 = cv2.inRange(hsv2, lower, upper)
		
		fgmask = mask - mask2
		
		# erode and dilate
		cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, numpy.ones((5,5)))
		
		# find contours in the thresholded image
		_, cnts, heirarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		cv2.imshow("Mask", fgmask)
		cv2.waitKey(0)
		
		contourLength  = len(cnts)
		# Check for at least one target found
		if contourLength < 1:
			return 0
			print("No target found")

		# target found
		## Loop through all of the contours, and get their areas
		area = [0.0]*contourLength
		for i in range(contourLength):
			area[i] = cv2.contourArea(cnts[i])

		#### Target #### the largest object
		c = cnts[area.index(max(area))]
		# show the output image
		cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
		cv2.imshow("Image", img)
		cv2.waitKey(0)
		# compute the center of the contour
		M = cv2.moments(c)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		print(cX,cY)
		
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
