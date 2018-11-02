import game_ttt.py
import ur5_control.py

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    rob = urx.Robot("192.168.1.5")
    rob.set_tcp((0,0,0,0,0,0))
    rob.set_payload(0.5, (0,0,0))
    try:
        l = 0.05
        v = 0.05
        a = 0.3
        #rob.movej([0.9760671854019165, -2.242768112813131, -1.423659626637594, -1.015625301991598, 1.5710539817810059, -0.13286143938173467],0.3,0.07)
        drawmap(rob)        
        rob.translate((-0.05,0,0),0.3,0.07)
        drawcross(rob)
        rob.translate((0.01,-0.01,0),0.3,0.07)
        drawcircle(rob)
    finally:
        rob.close()

print("Welcome to Tic Tac Toe!")

while True:
	#reset the board
	theBoard = ['']*10
	playerLetter,computerLetter = inputPlayerLetter()
	turn = whoGoesFirst()
	print('The'+turn+'will go first.')
	gameIsPlaying = True

	while gameIsPlaying:
		if turn == 'player':
			#Player's turn
			drawBoard(theBoard)
			move = getPlayerMove(theBoard)
			makeMove(theBoard,playerLetter,move)

			if isWinner(theBoard, playerLetter):
				drawBoard(theBoard)
				print('Congratulations! You have won the game!')
				gameIsPlaying = False
			else:
				if isBoardFull(theBoard):
					drawBoard(theBoard)
					print('The game is a tie!')
					break
				else:
					"Player's turn finished."
					turn = 'computer'
		else:
			#Computer's turn
			move = getComputerMove(theBoard, computerLetter)
			makeMove(theBoard, computerLetter, move)

			if isWinner(theBoard, computerLetter):
				drawBoard(theBoard)
				print('The computer has beaten you! You lose.')
				gameIsPlaying = False
			else:
				if isBoardFull(theBoard):
					drawBoard(theBoard)
					print('The game is a tie!')
					break
				else:
					turn = 'player'
	if not playAgain():
		break
