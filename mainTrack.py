from VideoCaptureClass import *
from TrackAndTransformFrames import TrackAndTransform
from generalConfig import *
import cv2
import time
import sys


def fillBufferToInitProcess(cap, trackObject, numbersOfFrames):
    for iterations in range(numbersOfFrames):
        ok, frame = cap.read()
        trackObject.fillBufferFrames(frame)

def requestPreparationsOfObject(trackObject):
    trackObject.requestRoi()
    trackObject.requestRoi()
    trackObject.requestTrackers()
    trackObject.requestTrackers()
    trackObject.startTrackers()
    trackObject.requestBackGroundSubtractors()
    trackObject.requestBackGroundSubtractors()

def mainFunction(width=1280, height=720):

    global cap #Verify the necessity TODO
    cap = AsyncVideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    cap.start()
    time.sleep(0.5) #giving time to camera up cool.

    trackTransformObj = TrackAndTransform(None, INITIAL_BUFFER_SIZE, TRASHOLD_CONTROLS, SIZE_REFERENC_TO_INTENSITY)
    fillBufferToInitProcess(cap, trackTransformObj, INITIAL_BUFFER_SIZE)

    requestPreparationsOfObject(trackTransformObj)

    while True:
        ok, frame = cap.read()
        ok, frame2 = cap.read()

        trackTransformObj.setFrame(frame)
        trackTransformObj.setGrayFrame(frame2)

        if ok:
            f1, intensityTurning, leftRight, intensityUpDown, upDown = trackTransformObj.updateTrackAndProcess()
            cv2.imshow('Frame', f1)
            # intensityTurning, leftRight, intensityUpDown, upDown
            sys.stdout.write(str(intensityTurning) + DELIMITER_TAGS + str(leftRight) + DELIMITER_TAGS +
                             str(intensityUpDown) + DELIMITER_TAGS + str(upDown) + '\n')

        if cv2.waitKey(1) == ord("q"):
            break

    cap.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    mainFunction(width=1280, height=720)

