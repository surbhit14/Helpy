import cv2
import mediapipe as mp
import math

mpHands = mp.solutions.hands
hands = mpHands.Hands()
drawTools = mp.solutions.drawing_utils

class HandDetector():
    def lmlist(self, img, draw = True):
        lmlist = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if(results.multi_hand_landmarks):
            for handlms in results.multi_hand_landmarks:
                for id, lm in enumerate(handlms.landmark):
                    h,w,c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)

                    lmlist.append([id,cx,cy])

                if draw:
                    drawTools.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)
        return lmlist, img


    def fingersUp(self, img, lmlist, draw = True):
        fingers = []
        tipIds = [8,12,16,20]
        count = 0
        if(lmlist[4][1] < lmlist[3][1]):
            fingers.append(1)
        else:
            fingers.append(0)
            count+=1
        
        for id in tipIds:
            if(lmlist[id][2] < lmlist[id - 2][2]):
                fingers.append(1)
                count+=1
            else:
                fingers.append(0)

        if draw:
            cv2.putText(img, str(fingers), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255),3)

        return fingers, img

    def findDistance(self, p1 , p2, img, lmlist, draw = False):
        x1,y1 = lmlist[p1][1:]
        x2,y2 = lmlist[p2][1:]

        cx, cy = (x1+x2)//2, (y1+y2)//2
        length = math.hypot(x2-x1, y2-y1)

        if(draw):
            cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
            cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

        return length, img

if __name__ == "__main__":
    detector = HandDetector()
    capture = cv2.VideoCapture(0)
    while True:
        success, img = capture.read()
        img = cv2.flip(img, 1)
        lmlist, img = detector.lmlist(img)

        if len(lmlist) != 0:
            fingers, img = detector.fingersUp(img,lmlist)
            print(fingers)

        cv2.imshow("Video Feed",img)
        key = cv2.waitKey(1)


   