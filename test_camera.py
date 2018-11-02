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



cap = cv2.VideoCapture("/dev/video28")

while(True):
	# Capture frame-by-frame
	ret, image = cap.read()
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	
	#find lines in the image
	lower = numpy.array([30,0,0],numpy.uint8)
	upper = numpy.array([179,100,80],numpy.uint8)
	mask = cv2.inRange(hsv, lower, upper)

	# dilate and erode
	mask2 = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, numpy.ones((26,26))) 
	# erode and dilate
	# mask3 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, numpy.ones((5,5)))
	
	# find lines
	lines = cv2.HoughLines(mask2,1,3*numpy.pi/180, 200)
	
	if lines.any()==None:
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
		print(rho, theta)
		# Horizontal
		if theta <= 3*numpy.pi/4 and theta > numpy.pi/4:
			if rhoH == 0:
				rhoH = rho
				lineH = ((x1,y1),(x2,y2))
			elif rho < rhoH-50:
				line0 = ((x1,y1),(x2,y2))
				line3 = lineH
			elif rho > rhoH+50:
				line3 = ((x1,y1),(x2,y2))
				line0 = lineH
		# Vertical
		else:
			rho = abs(rho)
			if rhoV == 0:
				rhoV = rho
				lineV = ((x1,y1),(x2,y2))
			elif rho < rhoV-50:
				line1 = ((x1,y1),(x2,y2))
				line2 = lineV
			elif rho > rhoV+50:
				line2 = ((x1,y1),(x2,y2))
				line1 = lineV
	
	# Display the resulting frame
	cv2.imshow('frame',image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
	try:
		p1 = line_intersection(line0, line1)
		p2 = line_intersection(line0, line2)
		p3 = line_intersection(line1, line3)
		p4 = line_intersection(line2, line3)
		
		if p1[1] < p3[1]:
			if p1[0] < p2[0]:
				A = p1
				B = p2 
				C = p3
				D = p4
			else:
				A = p2
				B = p1
				C = p4
				D = p3
		else:
			if p1[0] < p2[0]:
				A = p3
				B = p4
				C = p1
				D = p2
			else:
				A = p4
				B = p3
				C = p2
				D = p1
			
		for i in range(4):
			cap.grab()
		ret, image2 = cap.read()
		#cv2.imshow('frame2',image2)
		#if cv2.waitKey(1) & 0xFF == ord('q'):
		#	break
		
		bm = cv_ttt.boardMap(image2,A,B,C,D)
		
		# Capture new frame
		cv2.waitKey(0)
		for i in range(4):
			cap.grab()
		ret, image3 = cap.read()
		cv2.imshow('frame3',image3)		
		cv2.waitKey(0)

		print(bm.getUserPosition(image3))
		print(A,B,C,D)
		
		# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()
		break
		
	except Exception as e:
		import traceback
		traceback.print_exc()
		print(e)
		
	except KeyboardInterrupt:
		break
    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
