#[0.9760671854019165, -2.242768112813131, -1.423659626637594, -1.015625301991598, 1.5710539817810059, -0.13286143938173467]

import urx
import logging

def goToPoseInital():
    #rob.movej([0.9760671854019165, -2.242768112813131, -1.423659626637594, -1.015625301991598, 1.5710539817810059, -0.13286143938173467],0.3,0.07) 
    rob.movej(poseini)

def goToPosition(rob, pos):
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


def robupdown(rob,size=0.015,a=0.3,v=0.07):
    rob.translate((0,0,size),a,v)

def drawcross(rob):
    rob.translate((0.01,0,0),a,v)
    rob.translate((0,0,-0.015),a,v)
    #robupdown(rob,-0.015,a,v)
    rob.translate((size,0,0),a,v)
    rob.translate((0,0,0.01),a,v)
    #robupdown(rob,0.01,a,v)
    rob.translate((-size/2.0,size/2.0,0),a,v)
    #robupdown(rob,-0.01,a,v)
    rob.translate((0,0,-0.01),a,v)
    rob.translate((0,-size,0),a,v)
    #robupdown(rob,0.015,a,v)
    rob.translate((0,0,0.015),a,v)

def drawcircle(rob):
    rob.translate((0.01,0,0),a,v)
    rob.translate((0,0,-0.015),a,v)
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
    rob.translate((0,0,0.015),a,v)

def drawmap(rob):
    l = size*2.25
    rob.translate((l/3,l/3,0),a,v)

    rob.translate((0,0,-0.015),a,v)
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
    rob.translate((0,0,0.015),a,v)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.WARN)
        rob = urx.Robot("192.168.1.5")
        rob.set_tcp((0,0,0,0,0,0))
        rob.set_payload(0.5, (0,0,0))

        l = 0.05
        v = 0.05
        a = 0.3
        size = 0.04

        #Move the end point to the home position
        rob.translate((-0.07,-0.07,0.015),0.3,0.07)
        poseHome = rob.getj()

        #drawmap(rob)        
        #rob.translate((-0.05,0,0),0.3,0.07)
        #drawcross(rob)
        #rob.translate((0.01,-0.01,0),0.3,0.07)
        #drawcircle(rob)
    finally:
        rob.close()



