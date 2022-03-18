import math
from sre_constants import SUCCESS
import cvzone
import cv2
import random
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cam=cv2.VideoCapture(0)
# cam.set(3,1280)
# cam.set(4,720)

detector = HandDetector(detectionCon=0.8,maxHands=1)

class SnakeGameClass:
    def __init__(self,pathFood):
        self.points = [] #all points of the snake
        self.lengths = [] #distance between each points
        self.currentlength = 0 #total length of the snake
        self.allowedlength = 150 #total allowed length
        self.previoushead=0,0 #previous head point
        
        self.imgFood=cv2.imread(pathFood,cv2.IMREAD_UNCHANGED)
        self.hFood,self.wFood,_=self.imgFood.shape
        self.foodPoint= 0, 0
        self.randomFoodLocation()

    def randomFoodLocation(self):
        self.foodPoint=random.randint(100,400),random.randint(100,300)

    def update(self, imgMain, currentHead):
        px,py=self.previoushead
        cx,cy=currentHead
        self.points.append([cx,cy])
        distance=math.hypot(cx-px,cy-py)
        self.lengths.append(distance)
        self.currentlength+=distance
        self.previoushead=cx,cy


        # length reduction
        if self.currentlength > self.allowedlength:
            for i,length in enumerate(self.lengths):
                self.currentlength-=length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.currentlength < self.allowedlength:
                    break

        #drawing snake
        if self.points: 
            for i, point in enumerate(self.points):
                if i!=0:
                    cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),10)
            cv2.circle(img,self.points[-1],10,(200,0,200),cv2.FILLED)
        
        #draw food
        rx,ry=self.foodPoint
        cvzone.overlayPNG(imgMain,self.imgFood)
        
        return imgMain

game=SnakeGameClass()

while True:
    success,img=cam.read()
    img=cv2.flip(img,1)  #to flip the image of its not correct
    hands,img=detector.findHands( img , flipType=False) # to flip hand labels
    if hands:
        lmlist=hands[0]['lmList'] #list of all endpoints of
        pointIndex=lmlist[8][0:2]
        img=game.update(img,pointIndex)

    cv2.imshow("Image",img) 
    cv2.waitKey(1)