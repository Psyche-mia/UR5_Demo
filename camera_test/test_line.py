#!/usr/bin/env python
# Standard imports
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

img = cv2.imread('board.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
#cv2.imshow('houghlines3.jpg', gray)
#cv2.waitKey(0)
lines = cv2.HoughLines(edges,1,np.pi/180,200)

#store the line in (A,B),(C,D) matrix
line_points = []

#print(lines)
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
		cv2.imshow('houghlines3.jpg',img)
		cv2.waitKey(0)

cv2.imshow('houghlines3.jpg',img)
cv2.waitKey(0)

#cv2.imwrite('houghlines3.jpg',img)
#print (line_intersection(((1,2),(3,-1)),((3,-1),(4,0))))
#print(line_points)
A = line_intersection(line_points[0], line_points[2])
B = line_intersection(line_points[1], line_points[2])
C = line_intersection(line_points[0], line_points[3])
D = line_intersection(line_points[1], line_points[3])

print(A,B,C,D)
print(A[0],A[1])
#print(piont_A)