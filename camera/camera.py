import threading
import pickle
import numpy as np
import cv2
import time


class Camera:
    cap: cv2.VideoCapture
    undistort: bool = False
    thread: threading.Thread
    
    def __init__(self, port, auto_exposure = 1, resolution = (1920, 1080)):
        
        self.cap = cv2.VideoCapture(port)
    
        self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 127)
        self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, 127)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) # auto mode
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure) # manual mode
        # self.cap.set(cv2.CAP_PROP_EXPOSURE, 1)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        
        try:
            params_file = open(f"params.p", "rb")

            params = pickle.load(params_file)

            ret = params[0]
            self.mtx = params[1]
            self.dist = params[2]

            w, h = resolution
            self.newcameramtx, self.roi = cv2.getOptimalNewCameraMatrix(params[1], params[2], (w, h), 1, (w, h))
            
            self.undistort = True
            print("Params founded")
        except:
            print(f"No params to camera {port}")
            self.undistort = False
            
    def _start(self) -> None:
        while True:
            self.frame = self.cap.read()

    def start(self) -> None:
        
        self.thread = threading.Thread(target=self._start)
        self.thread.daemon = True
        print(2)
        self.thread.run()
        print(3)
        time.sleep(0.5)
        
    def read(self):
        flag, frame = self.cap.read()
        if not flag:
            return
        
        if self.undistort:
            dst = cv2.undistort(frame, self.mtx, self.dist, None, self.newcameramtx)
            h,  w = frame.shape[:2]
            x, y, w, h = self.roi
            frame = dst[y:y+h, x:x+w]
            
            pts_src = np.array([[842, 22], [807, 602], [221, 591], [229, 2]], dtype=np.float32)

            pts_dst = np.array([[0, 0], [w//2, 0], [w//2, h], [0, h]], dtype=np.float32)

            matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

            frame = cv2.warpPerspective(frame, matrix, (w//2, h))
            
        return frame
    
    
    
            
        
    def remove(self) -> None:
        self.cap.release()
        
            

        
    