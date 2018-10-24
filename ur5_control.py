#[0.9760671854019165, -2.242768112813131, -1.423659626637594, -1.015625301991598, 1.5710539817810059, -0.13286143938173467]

import urx
import logging


def drawcross(rob,size=0.04,a=0.3,v=0.05):
    rob.translate((0,0,-0.0152),a,v)
    rob.translate((size,0,0),a,v)
    rob.translate((0,0,0.01),a,v)
    rob.translate((-size/2.0,size/2.0,0),a,v)
    rob.translate((0,0,-0.01),a,v)
    rob.translate((0,-size,0),a,v)
    rob.translate((0,0,0.015),a,v)

def drawcircle(rob,size=0.04,a=0.3,v=0.05):
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

def drawmap(rob,size=0.04):
    l = size*9/4
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
    logging.basicConfig(level=logging.WARN)

    rob = urx.Robot("192.168.1.5")
    #rob = urx.Robot("localhost")
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



