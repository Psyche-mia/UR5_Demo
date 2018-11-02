import random
import urx
import logging

import cv2
import cv_ttt
import numpy

###### Camera ########
def getCurrentImage():
	for i in range(4):
		cap.grab()
	ret, image = cap.read()
	return image
	
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

	
def getABCD():
	while(True):
		# Capture frame-by-frame
		ret, image = cap.read()
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		#find lines in the image
		lower = numpy.array([30,0,0],numpy.uint8)
		upper = numpy.array([179,100,80],numpy.uint8)
		mask = cv2.inRange(hsv, lower, upper)

		# dilate and erode
		cv2.morphologyEx(mask, cv2.MORPH_CLOSE, numpy.ones((5,5))) 
		# erode and dilate
		cv2.morphologyEx(mask, cv2.MORPH_OPEN, numpy.ones((5,5)))

		# find lines
		lines = cv2.HoughLines(mask,1,3*numpy.pi/180, 200)

		if lines.any()==None:
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
	
		try:
			A = line_intersection(line0, line1)
			B = line_intersection(line0, line2)
			C = line_intersection(line1, line3)
			D = line_intersection(line2, line3)
	
			return A,B,C,D
	
		except Exception as e:
			import traceback
			traceback.print_exc()
			print(e)
		
		
###### Tic Tac Toe Gameplay ##########
def printBoard(s):
	print(" "+s[1]+" | "+s[2]+" | "+s[3])
	print(" "+s[4]+" | "+s[5]+" | "+s[6])
	print(" "+s[7]+" | "+s[8]+" | "+s[9])
	print()

def getPlayerMove(s):
	while True:
		pmove = int(input("Your turn. Make your move (1-9):"))
		if s[pmove]=='-':
			break
		print("Invalid move.")
	return pmove

def checkResult(s,p,rob, linedraw=False, size=0.04):
	l = size*2.25
	win = 0
	# diagonals
	if (s[1]==p and s[5]==p and s[9]==p):
		win = 1
		if linedraw:
			goToPosition(rob,1)
			rob.translate((l/3,-l/3,0),a,v)

			rob.translate((0,0,-paperdist),a,v)
			rob.translate((0,2*l,0),a,v)
			rob.translate((0,0,paperdist),a,v)

	elif (s[3]==p and s[5]==p and s[7]==p):
		win = 1
		if linedraw:
			goToPosition(rob,3)

			rob.translate((0,0,-paperdist),a,v)
			rob.translate((2*l,0,0),a,v)
			rob.translate((0,0,paperdist),a,v)
	else:
		for i in range(3):
			# rows
			if s[i*3+1]==p and s[i*3+2]==p and s[i*3+3]==p:
				win = 1
				if linedraw:
					goToPosition(rob,i*3+3)
					rob.translate((l/6,l/6,0),a,v)

					rob.translate((0,0,-paperdist),a,v)
					rob.translate((l,-l,0),a,v)
					rob.translate((0,0,paperdist),a,v)
				break
			# column
			elif s[i+1]==p and s[i+4]==p and s[i+7]==p:
				win = 1
				if linedraw:
					goToPosition(rob,i+1)
					rob.translate((l/6,-l/6,0),a,v)

					rob.translate((0,0,-paperdist),a,v)
					rob.translate((l,l,0),a,v)
					rob.translate((0,0,paperdist),a,v)
				break 

	if win:
		if p=='X':
			return 1    # X-win
		else:
			return 2    # O-win
	elif '-' not in s.values():
		return 3        # draw
	else:
		return 0        # game not ended
	

# X : return max value
# O : return min value
def minimax(s,p,rob):
	#initialize max/min
	if p == 'X':
		m = -10
	else:
		m = 10
		
	for i in range(1,10):
		if s[i] == '-':
			# evaluate each possible move
			s_next = s.copy()
			s_next[i] = p               
			result = checkResult(s_next,p,rob)
			
			if result == 0:
				# search if game not ended
				if p == 'X':
					val = minimax(s_next,'O',rob)
					if val > m:
						m = val
				elif p == 'O':
					val = minimax(s_next,'X',rob)
					if val < m:
						m = val            
			elif result == 1:
				m = 1     # X wins
				break
			elif result == 2:
				m = -1    # O wins
				break
			elif result == 3:
				m = 0     # draw
				break
			
	return m

def play(rob):
	result = 0
	s = {1:'-',2:'-',3:'-',
		 4:'-',5:'-',6:'-',
		 7:'-',8:'-',9:'-'}

	print("Welcome to Tic-Tac-Toe!")
	print()
	print("Board layout:")
	print(" 1 | 2 | 3 ")
	print(" 4 | 5 | 6 ")
	print(" 7 | 8 | 9 ")
	print()

	while True:
		p = input("X or O? (X goes first)\n")
		if p == 'X' or p == 'O':
			break

	if p == 'X':
		c = 'O'
		printBoard(s)

		rob.translate((homedist,homedist,0),a,v)
		drawMap(rob)
		
		# Initialize Board
		A,B,C,D = getABCD()
		print(A,B,C,D)
		mapImage = getCurrentImage()
		bm = cv_ttt.boardMap(mapImage,A,B,C,D)

		# player's turn
		cv2.waitKey(0)
		while True:
			updatedImage = getCurrentImage()
			pmove = bm.getUserPosition(updatedImage)
			if pmove != 0: 
				if s[pmove]=='-':
					break
		#pmove = getPlayerMove(s)
		s[pmove] = p
		printBoard(s)

		#goToPosition(rob,pmove)
		#drawcross(rob)
		#rob.movej(posHome,aj,vj)
		
	else:
		c = 'X'
		# optimal first move is a corner
		# (win if player do not put O in middle in next move)
		move = random.choice([1,3,7,9])
		s[move] = c
		print("Computer's turn.")
		printBoard(s)

		rob.translate((homedist,homedist,0),a,v)
		drawMap(rob)
		
		# Initialize Board
		A,B,C,D = getABCD()
		mapImage = getCurrentImage()
		bm = cv_ttt.boardMap(mapImage,A,B,C,D)

		# Draw computer's move
		goToPosition(rob,move)
		drawcross(rob)
		rob.movej(posHome,aj,vj)
		updatedImage = getCurrentImage()
		bm.updateSavedImage(updatedImage)


		# player's turn
		cv2.waitKey(0)
		while True:
			updatedImage = getCurrentImage()
			pmove = bm.getUserPosition(updatedImage)
			if pmove != 0: 
				if s[pmove]=='-':
					break
			#pmove = getPlayerMove(s)
		s[pmove] = p
		printBoard(s)

		#goToPosition(rob,pmove)
		#drawcircle(rob)
		#rob.movej(posHome,aj,vj)

	# While game not ended
	while result == 0:
		# Computer search for a move
		move = 0
		movelist = []
		
		#initialize max/min
		if c == 'X':
			m = -10
		else:
			m = 10
			
		for i in range(1,10):
			if s[i] == '-':
				# evaluate each possible move
				s_next = s.copy()
				s_next[i] = c               
				result = checkResult(s_next,c,rob) 

				# stop evaluating if game ended (draw on comp's turn or comp win)
				if result != 0:
					move = i
					break
				
				# search if game not ended
				if c == 'X':
					val = minimax(s_next,'O',rob)
					##print(val)
					if val > m:
						m = val
						movelist = [i]
					elif val == m:
						movelist.append(i)
				else:
					val = minimax(s_next,'X',rob)
					##print(val)
					if val < m:
						m = val
						movelist = [i]
					elif val == m:
						movelist.append(i)
				move = random.choice(movelist)
		
		# Computer makes move        
		s[move] = c
		print("Computer's turn.")
		printBoard(s)

		goToPosition(rob,move)
		if c=='X':
			drawcross(rob)
		else:
			drawcircle(rob)
		rob.movej(posHome,aj,vj)

		# Exit if game ended (draw on comp's turn or comp win)
		if result != 0:
			break
		
		updatedImage = getCurrentImage()
		bm.updateSavedImage(updatedImage)
		
		# Player makes move
		cv2.waitKey(0)
		while True:
			updatedImage = getCurrentImage()
			pmove = bm.getUserPosition(updatedImage)
			if pmove != 0: 
				if s[pmove]=='-':
					break
		#pmove = getPlayerMove(s)
		s[pmove] = p
		printBoard(s)

		#goToPosition(rob,pmove)
		#if p=='X':
		#    drawcross(rob)
		#else:
		#    drawcircle(rob)
		#rob.movej(posHome,aj,vj)

		# Exit if draw on player's turn or player win
		result = checkResult(s,p,rob) 

	# Game ended, print results
	if result==1:
		print("X wins!")
		result = checkResult(s,'X',rob,True) 
	elif result==2:
		print("O wins!")
		result = checkResult(s,'O',rob,True) 
	elif result==3:
		print("It's a draw!")

	rob.movej(posHome,aj,vj)


def goToPosition(rob, pos):
	rob.movej(posHome,aj,vj)
	rob.translate((homedist,homedist,0),a,v)

	s = size*1.5
	if pos == 9:
		rob.translate((s,s,0),a,v)
	elif pos == 8:
		rob.translate((s*1.5,s*0.5,0),a,v)
	elif pos == 7:
		rob.translate((s*2,0,0),a,v)
	elif pos == 6:
		rob.translate((s*0.5,s*0.5,0),a,v)
	elif pos == 5:
		rob.translate((s,0,0),a,v)
	elif pos == 4:
		rob.translate((s*1.5,-s*0.5,0),a,v)
	elif pos == 3:
		pass
	elif pos == 2:
		rob.translate((s*0.5,-s*0.5,0),a,v)
	elif pos == 1:
		rob.translate((s,-s,0),a,v)


def drawcross(rob):
	rob.translate((size/4,0,0),a,v)

	rob.translate((0,0,-paperdist),a,v)
	rob.translate((size,0,0),a,v)
	rob.translate((0,0,0.01),a,v)
	rob.translate((-size/2.0,size/2.0,0),a,v)

	rob.translate((0,0,-0.01),a,v)
	rob.translate((0,-size,0),a,v)
	rob.translate((0,0,paperdist),a,v)

def drawcircle(rob):
	rob.translate((size/2.66667,0,0),a,v)
	rob.translate((0,0,-paperdist),a,v)
	pose = rob.getl()
	pose1 = pose[:]
	pose2 = pose[:]
	c = 2**0.5
	pose1[0] += size/2.0/c
	pose1[1] += size/2.0/c
	pose2[0] += size/c
	rob.movec(pose1,pose2,a,v)
	pose1[1] -= size/c
	rob.movec(pose1,pose,a,v)
	rob.translate((0,0,paperdist),a,v)

def drawMap(rob):
	l = size*2.25
	rob.translate((l/3,l/3,0),a,v)

	rob.translate((0,0,-paperdist),a,v)
	rob.translate((l,-l,0),a,v)
	rob.translate((0,0,0.01),a,v)
	rob.translate((l/3,l/3,0),a,v)

	rob.translate((0,0,-0.01),a,v)
	rob.translate((-l,l,0),a,v)
	rob.translate((0,0,0.01),a,v)
	rob.translate((2*l/3,0,0),a,v)

	rob.translate((0,0,-0.01),a,v)
	rob.translate((-l,-l,0),a,v)
	rob.translate((0,0,0.01),a,v)
	rob.translate((l/3,-l/3,0),a,v)

	rob.translate((0,0,-0.01),a,v)
	rob.translate((l,l,0),a,v)
	rob.translate((0,0,paperdist),a,v)
	rob.movej(posHome,aj,vj)

if __name__ == "__main__":
	try:
		# bring up camera
		cap = cv2.VideoCapture("/dev/video27")
		
		logging.basicConfig(level=logging.WARN)
		rob = urx.Robot("192.168.1.5")
		rob.set_tcp((0,0,0,0,0,0))
		rob.set_payload(0.5, (0,0,0))

		#l = 0.05
		v = 0.1
		a = 0.4
		aj = 1.8
		vj = 0.5
		size = 0.04
		homedist = 0.07
		paperdist = 0.0158

		# Move the end point to the home position
		# Current posHome = [1.014582,-1.669491,-2.249615,-0.846732,1.599876,-0.220884]

		# If robot is not currently homed, 
		# place marker tip touching bottom left corner of the map and uncomment the line below.
		#rob.translate((-homedist,-homedist,paperdist),a,v)

		#rob.translate((homedist,homedist,-paperdist),a,v)
		#rob.translate((-0.09,-0.09,0),a,v)
		#rob.translate((-homedist,-homedist,0.001),a,v)
		
		#rob.translate((-0.22,-0.10,0),a,v) 
		posHome = rob.getj()
		print(posHome)
		while True:
			play(rob)
			newgame = input("Do you want to play again? (y/n)")
			print()
			rob.movej(posHome,aj,vj)
			if newgame == 'n':
				break
	finally:
		rob.close()
		# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()
