import random
import urx
import logging

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

        # player's turn
        pmove = getPlayerMove(s)
        s[pmove] = p
        printBoard(s)

        goToPosition(rob,pmove)
        drawcross(rob)
        rob.movej(posHome,aj,vj)
        
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

        goToPosition(rob,move)
        drawcross(rob)
        rob.movej(posHome,aj,vj)


        # player's turn
        pmove = getPlayerMove(s)
        s[pmove] = p
        printBoard(s)

        goToPosition(rob,pmove)
        drawcircle(rob)
        rob.movej(posHome,aj,vj)

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
        
        # Player makes move
        pmove = getPlayerMove(s)
        s[pmove] = p
        printBoard(s)

        goToPosition(rob,pmove)
        if p=='X':
            drawcross(rob)
        else:
            drawcircle(rob)
        rob.movej(posHome,aj,vj)

        # Exit if draw on player's turn or player win
        result = checkResult(s,p) 

    # Game ended, print results
    if result==1:
        print("X wins!")
    elif result==2:
        print("O wins!")
    elif result==3:
        print("It's a draw!")


def goToPosition(rob, pos):
    rob.movej(posHome,aj,vj)
    rob.translate((homedist,homedist,0),a,v)

    s = size*1.5
    if pos == 1:
        rob.translate((s,s,0),a,v)
    elif pos == 2:
        rob.translate((s*1.5,s*0.5,0),a,v)
    elif pos == 3:
        rob.translate((s*2,0,0),a,v)
    elif pos == 4:
        rob.translate((s*0.5,s*0.5,0),a,v)
    elif pos == 5:
        rob.translate((s,0,0),a,v)
    elif pos == 6:
        rob.translate((s*1.5,-s*0.5,0),a,v)
    elif pos == 7:
        pass
    elif pos == 8:
        rob.translate((s*0.5,-s*0.5,0),a,v)
    elif pos == 9:
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
    pose1 = pose.copy()
    pose2 = pose.copy()
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

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.WARN)
        rob = urx.Robot("192.168.1.5")
        rob.set_tcp((0,0,0,0,0,0))
        rob.set_payload(0.5, (0,0,0))

        #l = 0.05
        v = 0.07
        a = 0.3
        aj = 1.5
        vj = 0.35
        size = 0.04
        homedist = 0.07
        paperdist = 0.015

        # Move the end point to the home position
        # Current posHome = [1.014582,-1.669491,-2.249615,-0.846732,1.599876,-0.220884]

        # If robot is not currently homed, 
        # place marker tip touching bottom left corner of the map and uncomment the line below.
        #rob.translate((-homedist,-homedist,paperdist),a,b) 
        posHome = rob.getj()

        while True:
            play(rob)
            newgame = input("Do you want to play again? (y/n)")
            print()
            rob.movej(posHome,aj,vj)
            if newgame == 'n':
                break
    finally:
        rob.close()
