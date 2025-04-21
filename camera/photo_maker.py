import cv2
from threading import Thread
from camera import Camera
import time
import os

path = '/home/barash/projects/VSOSH_python/camera/samples'

camera = Camera(0)
camera.undistort = False

def click(event, x, y, flags, param):

	if event == cv2.EVENT_LBUTTONDOWN:
		cv2.imwrite(os.path.join(path , f'{time.time()}_{x}{y}.jpg'), camera.read())
  
cv2.namedWindow('frame')
cv2.setMouseCallback('frame',click)

time.sleep(5)

while True:
    frame = camera.read()
    print(frame.shape)
    # shown = cv2.resize(frame, (640, 480))
    
    cv2.imwrite(os.path.join(path , f'{time.time()}.jpg'), camera.read())
    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1000) == ord('q'):
        break
    