import random

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

def checkResult(s,p):
    win = 0
    # diagonals
    if (s[1]==p and s[5]==p and s[9]==p) or (s[3]==p and s[5]==p and s[7]==p):
        win = 1
    else:
        for i in range(3):
            # rows
            if s[i*3+1]==p and s[i*3+2]==p and s[i*3+3]==p:
                win = 1
                break
            # column
            elif s[i+1]==p and s[i+4]==p and s[i+7]==p:
                win = 1
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
def minimax(s,p):
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
            result = checkResult(s_next,p)
            
            if result == 0:
                # search if game not ended
                if p == 'X':
                    val = minimax(s_next,'O')
                    if val > m:
                        m = val
                elif p == 'O':
                    val = minimax(s_next,'X')
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

def play():
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

        # player's turn
        pmove = getPlayerMove(s)
        s[pmove] = p
        printBoard(s)
        
    else:
        c = 'X'
        # optimal first move is a corner
        # (win if player do not put O in middle in next move)
        move = random.choice([1,3,7,9])
        s[move] = c
        print("Computer's turn.")
        printBoard(s)

        # player's turn
        pmove = getPlayerMove(s)
        s[pmove] = p
        printBoard(s)

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
                result = checkResult(s_next,c) 

                # stop evaluating if game ended (draw on comp's turn or comp win)
                if result != 0:
                    move = i
                    break
                
                # search if game not ended
                if c == 'X':
                    val = minimax(s_next,'O')
                    ##print(val)
                    if val > m:
                        m = val
                        movelist = [i]
                    elif val == m:
                        movelist.append(i)
                else:
                    val = minimax(s_next,'X')
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
        ##print(s)
        printBoard(s)
        # Exit if game ended (draw on comp's turn or comp win)
        if result != 0:
            break
        
        # Player makes move
        pmove = getPlayerMove(s)
        s[pmove] = p
        printBoard(s)
        # Exit if draw on player's turn or player win
        result = checkResult(s,p) 

    # Game ended, print results
    if result==1:
        print("X wins!")
    elif result==2:
        print("O wins!")
    elif result==3:
        print("It's a draw!")

while True:
    play()
    newgame = input("Do you want to play again? (y/n)")
    print()
    if newgame == 'n':
        break
    
