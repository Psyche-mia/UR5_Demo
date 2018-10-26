import numpy
import cv2
import cv_ttt

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



cap = cv2.VideoCapture(1)

while(True):
	# Capture frame-by-frame
	ret, image = cap.read()
	width, height =image.shape[:2]
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
	
	_, contours, heirarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
	
	#gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#edges = cv2.Canny(gray,25,50,apertureSize = 3)
	#lines = cv2.HoughLines(edges,5,5*numpy.pi/180,300)

	
	if lines==None:
		cv2.imshow('frame',image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		continue
		
	#if len(lines) != 4:
		#continue
		
	#store the line in (A,B),(C,D) matrix
	line_points = []
	
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
		line_points.append(((x1,y1),(x2,y2)))
		
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
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
	try:
		#A = line_intersection(line_points[0], line_points[1])
		#B = line_intersection(line_points[0], line_points[2])
		#C = line_intersection(line_points[1], line_points[3])
		#D = line_intersection(line_points[2], line_points[3])
		A = line_intersection(line0, line1)
		B = line_intersection(line0, line2)
		C = line_intersection(line1, line3)
		D = line_intersection(line2, line3)
		bm = cv_ttt.boardMap(mask,A,B,C,D)
		print(A,B,C,D)
		
	except Exception as e:
		print(e)
    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
