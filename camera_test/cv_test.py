#!/usr/bin/env python
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
# import the necessary packages
#import imutils
import cv2
import numpy as np


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

class boardMap():
	def __init__(self):
		# initialize ROS node
		rospy.init_node('target_detector', anonymous=True)
		
		# Convert image from a ROS image message to a CV image
		self.bridge = CvBridge()

		# Wait for the camera_info topic to become available
		rospy.wait_for_message('/camera/rgb/image_raw', Image)

		# Subscribe to registered color image
		rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback, queue_size=1)
		
	def image_callback(self, msg):

		# convert ROS image to OpenCV image
		try:
			img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
		except CvBridgeError as e:
			print(e)
			
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray,50,150,apertureSize = 3)
		lines = cv2.HoughLines(edges,1,np.pi/180,200)

		#store the line in (A,B),(C,D) matrix
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
				cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
				cv2.imshow("Lines",img)
		
		self.A = line_intersection(line_points[0], line_points[2])
		self.B = line_intersection(line_points[1], line_points[2])
		self.C = line_intersection(line_points[0], line_points[3])
		self.D = line_intersection(line_points[1], line_points[3])
		self.savedImage = img
		cv2.waitKey(0)
		
		try:
			img2 = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
		except CvBridgeError as e:
			print(e)
		print(self.getUserPosition(img2))

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
		#cnts = cnts[0] if imutils.is_cv2() else cnts[1]

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


if __name__ == '__main__':
	# start up the detector node and run until shutdown by interrupt
	try:
		boardMap = boardMap()
		rospy.spin()

	except rospy.ROSInterruptException:
		rospy.loginfo("Detector node terminated.")

	# close all terminal windows when process is shut down
	cv2.destroyAllWindows()
   
