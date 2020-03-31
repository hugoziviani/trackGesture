import cv2
import math
import numpy as np

def distanceRange(x1,y1,x2,y2):  
     distance = float(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
     return distance

if __name__ == '__main__':
    backSub = cv2.createBackgroundSubtractorKNN(history=1, detectShadows=False)
    backSub2 = cv2.createBackgroundSubtractorKNN(history=1, detectShadows=False)
    #backSub = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=150, detectShadows=False)

    tracker = cv2.TrackerMIL_create()
    tracker2 = cv2.TrackerMIL_create()
    
    video = cv2.VideoCapture(0)

    ok, frame = video.read()
    vetFrames = []
    for i in range(60):
        ok, frame = video.read()
        frame = cv2.flip(frame, 1)
        vetFrames.append(frame)

    color = (0, 255, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    vetFrames[57] = cv2.putText(vetFrames[57], 'Select your first control region:', (50,50), font, 1, color, 1, cv2.LINE_AA) 
    
    bbox = cv2.selectROI(vetFrames[57], True)
    
    vetFrames[58] = cv2.putText(vetFrames[58], 'Select your second control region:', (50,50), font, 1, color, 1, cv2.LINE_AA) 
    bbox2 = cv2.selectROI(vetFrames[58], True)
    
    bboxDefault = bbox
    bboxDefault2 = bbox2

    gray = cv2.cvtColor(vetFrames[50], cv2.COLOR_BGR2GRAY)
    
    ok = tracker.init(gray, bbox)
    ok = tracker2.init(frame, bbox2)

    while True:
        ok, frame = video.read()
        ok, frame2 = video.read()
        if not ok: exit()
                
        frame = cv2.flip(frame, 1)
        frame2 = cv2.flip(frame2, 1)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray, (3, 3))

        
        
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        x2, y2, w2, h2 = int(bbox2[0]), int(bbox2[1]), int(bbox2[2]), int(bbox2[3])
        
        roi = frame[y:y + h, x:x + w]
        roi2 = frame[y2:y2 + h2, x2:x2 + w2]
        
        roiGray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roiGray2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("roiGray", roiGray)
        #cv2.imshow("roiGray2", roiGray2)
        
        roiBlur = cv2.GaussianBlur(roiGray, (3,3),3,0)
        roiBlur2 = cv2.GaussianBlur(roiGray2, (3,3),3,0)
        #cv2.imshow("roiBlur", roiBlur)
        #cv2.imshow("roiBlur2", roiBlur2)

        fgMask = backSub.apply(roiBlur)
        fgMask2 = backSub2.apply(roiBlur2)
        #cv2.imshow("fgMask", fgMask)
        #cv2.imshow("fgMask2", fgMask2)
        
        contours, hierarchy = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours2, hierarchy2 = cv2.findContours(fgMask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if (len(contours2) + len(contours) > 2):
            ok, bbox = tracker.update(blur)
            ok, bbox2 = tracker2.update(frame)
        
        p1 = (x, y)
        p2 = (x + w, y + h)
        xCenter = round(x + w / 2)
        yCenter = round(y + h / 2)
        
        color = (0, 5, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        image = cv2.putText(frame, 'TR-1', (x,y), font, 1, color, 2, cv2.LINE_AA) 

        p1_2 = (x2, y2)
        p2_2 = (x2 + w2, y2 + h2)
        xCenter2 = round(x2 + w2 / 2)
        yCenter2 = round(y2 + h2 / 2)
        image = cv2.putText(frame, 'TR-2', (x2,y2), font, 1, color, 2, cv2.LINE_AA)

        cv2.line(frame, p1, p2, (255, 0, 255), 4)
        cv2.circle(frame, (xCenter, yCenter), 5, (0, 255, 0), -2)
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

        cv2.line(frame, p1_2, p2_2, (100, 250, 0), 4)
        cv2.circle(frame, (xCenter2, yCenter2), 5, (0, 100, 200), -2)
        cv2.rectangle(frame, p1_2, p2_2, (255, 0, 0), 2, 1)


        xBeg, yBeg, wBeg, hBeg = int(bboxDefault[0]), int(bboxDefault[1]), int(bboxDefault[2]), int(bboxDefault[3])
        x2Beg, y2Beg, w2Beg, h2Beg = int(bboxDefault2[0]), int(bboxDefault2[1]), int(bboxDefault2[2]), int(bboxDefault2[3])
        
        xCenterBeg = round(xBeg + wBeg / 2)
        yCenterBeg = round(yBeg + hBeg / 2)
        cv2.circle(frame, (xCenterBeg, yCenterBeg), 40, (0, 0, 255), 2)
        cv2.circle(frame, (xCenterBeg, yCenterBeg), 6, (0, 0, 255), 3)
        cv2.line(frame, (xCenterBeg, yCenterBeg), (xCenter, yCenter), (255, 0, 255), 2)
        distanceRange(xBeg, yBeg, xCenter, yCenter)

        xCenter2Beg = round(x2Beg + w2Beg / 2)
        yCenter2Beg = round(y2Beg + h2Beg / 2)
        cv2.circle(frame, (xCenter2Beg, yCenter2Beg), 40, (0, 0, 255), 2)
        cv2.circle(frame, (xCenter2Beg, yCenter2Beg), 6, (0, 0, 255), 3)
        cv2.line(frame, (xCenter2Beg, yCenter2Beg), (xCenter2, yCenter2), (255, 0, 255), 2)
        #print ("X-XTrace", (xCenter-xBeg)*(-1))
        print ("yCenter:", yCenter)
        print ("yBeg:", yBeg)
        print ("Y-YTrace", (yCenter-yBeg)*(-1))
        cv2.imshow("Frame", frame)

        k = cv2.waitKey(1)
        if k == ord('q'):
            exit()
cv2.destroyAllWindows()
