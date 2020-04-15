from threading import Thread, Lock
import cv2

class AsyncVideoCapture:
    def __init__(self, src=0, width=1280, height=720):
        print('Building VideoCaptureAsync Class to capture')
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.readLock = Lock()

    def set(self, frameSize, frameSize2):
        self.cap.set(frameSize, frameSize2)

    def start(self):
        if self.started:
            print('Async capture started.')
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.readLock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.readLock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()