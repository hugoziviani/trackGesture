import sys
import cv2
from queue import Queue
import math

class TrackAndTransform:
    def __init__(self, frame=None, bufferFramesSize=500, trasholdControls=40, sizeRefferenceToIntensitys=40):
        print('Building TrackAndTransform Class...')
        try:
            self.previousFrame = None
            self.frame = frame
            self.grayFrame = None
            self.frameBuffer = Queue(bufferFramesSize)
            self.ROIs = []
            self.DefaultROIs = []
            self.backGroundsSubtractors = []
            self.trackers = []
            self.trasholdControl = trasholdControls
            self.sizeRefferenceToIntensity = sizeRefferenceToIntensitys
            self.tracSquares = []
            self.intensityTurning = None
            self.intensityUpDown = None
        except:
            print("Error ", sys.exc_info())

    def setFrame(self, frame):
        self.frame = frame

    def setGrayFrame(self, frame):
        self.grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def getFrame(self):
        return cv2.flip(self.frame, 1)

    def getGrayFrame(self):
        return cv2.flip(self.grayFrame, 1)

    def fillBufferFrames(self, frameR):
        try:
            self.frameBuffer.put(frameR)
        except:
            #print("incheu", self.frameBuffer.qsize())
            pass

    def requestRoi(self):
        #is possible add more ROIS
        color = (0, 255, 5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame = cv2.putText(cv2.flip(self.frameBuffer.get(), 1), 'Select your ' + str(len(self.ROIs)+1) + ' control region:', (50, 50), font, 1, color, 1, cv2.LINE_AA)
        bbox = cv2.selectROI(frame, True)
        self.ROIs.append(bbox)
        self.DefaultROIs.append(bbox)

    def requestBackGroundSubtractors(self, history=1, detectShadows=False):
        self.backGroundsSubtractors.append(cv2.createBackgroundSubtractorKNN(history=history, detectShadows=detectShadows))
        #cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=150, detectShadows=False)
        return len(self.backGroundsSubtractors)

    def requestTrackers(self):
        tracker = cv2.TrackerMIL_create()
        if tracker:
            self.trackers.append(tracker)
            print("Tracker ", len(self.trackers), "created at", tracker)

    def startTrackers(self):
        frameToStartTrack = self.frameBuffer.get()
        for tracker, roi in zip(self.trackers, self.ROIs):
            print("Starting:", tracker)
            tracker.init(frameToStartTrack, roi)

    def updatePreviousFrame(self, frame):
        self.previousFrame = frame

    def updateTrackAndProcess(self):
        frame = self.getFrame()
        gray = self.getGrayFrame()

        blur = cv2.blur(gray, (3, 3))

        bbox = self.ROIs[0]
        bbox2 = self.ROIs[1]

        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        x2, y2, w2, h2 = int(bbox2[0]), int(bbox2[1]), int(bbox2[2]), int(bbox2[3])

        roiGray1 = blur[y:y + h, x:x + w]
        roiGray2 = blur[y2:y2 + h2, x2:x2 + w2]

        roiBlur1 = cv2.GaussianBlur(roiGray1, (3, 3), 3, 0)
        roiBlur2 = cv2.GaussianBlur(roiGray2, (3, 3), 3, 0)

        fgMask1 = self.backGroundsSubtractors[0].apply(roiBlur1)
        fgMask2 = self.backGroundsSubtractors[1].apply(roiBlur2)

        contours, hierarchy = cv2.findContours(fgMask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours2, hierarchy2 = cv2.findContours(fgMask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if (len(contours2) + len(contours) > 2):
            ok, self.ROIs[0] = self.trackers[0].update(blur)
            ok, self.ROIs[1] = self.trackers[1].update(frame)

        p1 = (x, y)
        p2 = (x + w, y + h)
        xCenter = round(x + w / 2)
        yCenter = round(y + h / 2)

        color = (0, 5, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        image = cv2.putText(frame, 'Right/Left', (x, y), font, 1, color, 2, cv2.LINE_AA)

        p1_2 = (x2, y2)
        p2_2 = (x2 + w2, y2 + h2)
        xCenter2 = round(x2 + w2 / 2)
        yCenter2 = round(y2 + h2 / 2)
        image = cv2.putText(frame, 'Up/Down', (x2, y2), font, 1, color, 2, cv2.LINE_AA)

        p1_2 = (x2, y2)
        p2_2 = (x2 + w2, y2 + h2)
        xCenter2 = round(x2 + w2 / 2)
        yCenter2 = round(y2 + h2 / 2)
        image = cv2.putText(frame, 'Up/Down', (x2, y2), font, 1, color, 2, cv2.LINE_AA)

        # cv2.line(frame, p1, p2, (255, 0, 255), 4)
        cv2.circle(frame, (xCenter, yCenter), 5, (0, 255, 0), -2)
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

        # cv2.line(frame, p1_2, p2_2, (100, 250, 0), 4)
        cv2.circle(frame, (xCenter2, yCenter2), 5, (0, 100, 200), -2)
        cv2.rectangle(frame, p1_2, p2_2, (255, 0, 0), 2, 1)

        bboxDefault = self.DefaultROIs[0]
        bboxDefault2 = self.DefaultROIs[1]

        xBeg, yBeg, wBeg, hBeg = int(bboxDefault[0]), int(bboxDefault[1]), int(bboxDefault[2]), int(bboxDefault[3])
        x2Beg, y2Beg, w2Beg, h2Beg = int(bboxDefault2[0]), int(bboxDefault2[1]), int(bboxDefault2[2]), int(bboxDefault2[3])

        xBeg, yBeg, wBeg, hBeg = int(bboxDefault[0]), int(bboxDefault[1]), int(bboxDefault[2]), int(
            bboxDefault[3])
        x2Beg, y2Beg, w2Beg, h2Beg = int(bboxDefault2[0]), int(bboxDefault2[1]), int(bboxDefault2[2]), int(
            bboxDefault2[3])

        xCenterBeg = round(xBeg + wBeg / 2)
        yCenterBeg = round(yBeg + hBeg / 2)
        cv2.circle(frame, (xCenterBeg, yCenterBeg), self.trasholdControl, (0, 0, 255), 2)
        cv2.circle(frame, (xCenterBeg, yCenterBeg), 6, (0, 0, 255), 3)
        cv2.line(frame, (xCenterBeg, yCenterBeg), (xCenter, yCenter), (255, 0, 255), 2)

        xCenter2Beg = round(x2Beg + w2Beg / 2)
        yCenter2Beg = round(y2Beg + h2Beg / 2)
        cv2.circle(frame, (xCenter2Beg, yCenter2Beg), self.trasholdControl, (0, 0, 255), 2)
        cv2.circle(frame, (xCenter2Beg, yCenter2Beg), 6, (0, 0, 255), 3)
        cv2.line(frame, (xCenter2Beg, yCenter2Beg), (xCenter2, yCenter2), (255, 0, 255), 2)

        turningStraight = self.__distanceRange(xCenterBeg, yCenterBeg, xCenter, yCenter)
        self.intensityTurning = self.__percentIntensity(self.sizeRefferenceToIntensity, turningStraight)
        sizeStraight = self.__distanceRange(xCenter2Beg, yCenter2Beg, xCenter2, yCenter2)
        self.intensityUpDown = self.__percentIntensity(self.sizeRefferenceToIntensity, sizeStraight)

        leftRight = xCenterBeg - xCenter
        upDown = yCenter2Beg - yCenter2

        self.__afferDirections(leftRight, upDown)

        self.updatePreviousFrame(self.frame)# to keep if need
        return frame

    def __distanceRange(self, x1, y1, x2, y2):
        distance = float(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        return distance

    def __percentIntensity(self, defaultThreshControl, straightSize):
        return float(straightSize / defaultThreshControl)

    def __afferDirections(self, leftRight, upDown):

        if (leftRight < self.trasholdControl * (-1)):
            print("indo p esquerda: ", leftRight)
            print("Left Percent: ", self.intensityTurning)
        if (leftRight > self.trasholdControl):
            print("indo p direita: ", leftRight)
            print("Right Percent: ", self.intensityTurning)
        if (leftRight > self.trasholdControl * (-1) and leftRight < self.trasholdControl):
            print("Paradin da silva: ", leftRight)

        if (upDown < self.trasholdControl * (-1)):
            print("indo p baixo: ", upDown)
            print("Down Percent: ", self.intensityUpDown)
        if (upDown > self.trasholdControl):
            print("indo p cima: ", upDown)
            print("Upp Percent: ", self.intensityUpDown)
        if (upDown > self.trasholdControl * (-1) and upDown < self.trasholdControl):
            print("sem andar: ", upDown)