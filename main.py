from multiprocessing.connection import wait
from sre_constants import SUCCESS
from time import sleep
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cam=cv2.VideoCapture(0)
# cam.set(3,1280)
# cam.set(4,720)

detector = HandDetector(detectionCon=0.8,maxHands=1)

while True:
    success,img=cam.read()
    img=cv2.flip(img,1)  #to flip the image of its not correct
    hands,img=detector.findHands( img , flipType=False) # to flip hand labels
    if hands:
        lmlist=hands[0]['lmList'] #list of all endpoints of
        pointIndex=lmlist[8][0:2]
        cv2.circle(img,pointIndex,20,(200,0,200),cv2.FILLED)

    cv2.imshow("Image",img) 
    cv2.waitKey(1)