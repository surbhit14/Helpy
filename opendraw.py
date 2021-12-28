import cv2
import numpy as np
import os
from handtrackingmodule import HandDetector

bt=5 #thickness of brush
et=100 #thickness of eraser

folderPath="head1"
l=os.listdir(folderPath)
imgl= []
for i in l:
    image = cv2.imread(f'{folderPath}/{i}')
    imgl.append(image)


header1=imgl[0]
header2=imgl[6]

pc=(255, 0, 255)#paint color

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector()
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
r=1
c=0
font = cv2.FONT_HERSHEY_SIMPLEX
i=10


while True:
    # Import the image
    sc, img = cap.read()
    img = cv2.flip(img, 1)

    # Find the Hand Landmarks 
    lmList, img = detector.lmlist(img)
    k = cv2.waitKey(33)

    if len(lmList) != 0:
        # tip of index finger
        x1, y1 = lmList[8][1:]
        # tip of  middle finger
        x2, y2 = lmList[12][1:]

        # Find fingers which  are up
        fingers, img = detector.fingersUp(img, lmList, False)
        

        # Selection Mode (index and middle finger are up)
        if fingers[1] and fingers[2]:
            #xp, yp = 0, 0
            if y1<133:

                #free draw
                if 10<x1<150:
                    header1=imgl[0]
                    r=1

                #text
                elif 155<x1<365:
                    header1=imgl[1]
                    r=2

                #rectangle
                elif 375<x1<610:
                    header1=imgl[2]
                    r=3

                #line
                elif 615<x1<755:
                    header1=imgl[3]
                    r=4

                #eraser  
                elif 758<x1<928:
                    header1=imgl[4]
                    pc = (0,0,0)
                    r=5

                #sign_language
                elif 935<x1<1140:

                    header1=imgl[5]
                    r=6
                
            
            if x1>1150:
                if 120<y1<290:
                    pc = (0,0,255)#red color
                    header2=imgl[6]
                    
                    
                elif 350<y1<500:
                    pc = (0,128,0)#green color
                    header2=imgl[7]
                
                elif 530<y1<680:
                    pc=(255, 0, 255)#pink color
                    header2=imgl[8]

                    
            cv2.rectangle(img, (x1, y1 - 30), (x2, y2+30), pc, cv2.FILLED)

      
        if r==1 or r==5:
            if fingers==[0,1,0,0,0]:
            #if fingers[1]== True and fingers[2]==False:
                cv2.circle(img, (x1, y1), 15, pc, cv2.FILLED)
                #print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                    cv2.line(img, (xp, yp), (x1, y1), pc, bt)

                if pc == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), pc, et)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), pc, et)
                
                else:
                    cv2.line(img, (xp, yp), (x1, y1), pc, bt)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), pc, bt)
            xp, yp = x1, y1
        
        elif r==2:
            if k==27:
                break    # Esc key to stop
                
            elif k==-1:
                xd,yd=x1,y1
                pass 
                
            else:
                cv2.putText(imgCanvas, chr(k), (xd,yd), font, 1.8, (0, 255, 0), 1, cv2.LINE_AA)
                xd+=15

        elif r==3 or r==4:
            # Wait point
            if (k==-1):
                #cv2.circle(img, (x1, y1), 15, pc, cv2.FILLED)
                cv2.putText(img,"waiting", (200,200),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                cv2.waitKey(15)
                pass

            # Selecting points (Index finger is up)
            else:
                if fingers==[0,1,1,0,0] or fingers==[0,1,0,0,0] or True:
                    if(c==1):
                        if(r==4):
                            cv2.line(img,(xp, yp),(x1, y1), pc, bt)
                            cv2.line(imgCanvas, (xp, yp),(x1, y1), pc,bt)
                        else:
                            cv2.rectangle(img,(xp, yp),(x1, y1), pc, bt)
                            cv2.rectangle(imgCanvas, (xp, yp),(x1, y1), pc,bt)

                        cv2.waitKey(15)
                        c=0
                    else:
                        xp,yp=x1,y1
                        c=1
                        cv2.waitKey(15)

        elif r==6:
            if fingers==[0,1,0,0,0]:
                cv2.putText(img,"Hello ", (200,200),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            
            elif fingers==[0,1,1,0,0]:
                cv2.putText(img,"How are you? ", (200,200),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
 
            elif fingers==[0,1,1,1,0]:
                cv2.putText(img,"I am fine", (200,200),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            
            elif fingers==[0,1,1,1,1]:
                cv2.putText(img,"Thank You ", (200,200),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

            elif fingers==[0,1,1,1,1]:
                cv2.putText(img,"Please explain", (200,200),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            
            elif fingers==[1,0,0,0,0]:
                cv2.putText(img,"Ok", (200,200),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)


    img[0:130,0:1280] = header1
    img[120:720,1150:1280]=header2
    cv2.imshow("Image", img)
    
    cv2.waitKey(1)