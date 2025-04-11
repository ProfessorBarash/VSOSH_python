import cv2
from threading import Thread
from camera import Camera
import time
import os

path = '/home/nto-pc/projects/IRS_final/camera/samples'

cap = cv2.VideoCapture("http://root:admin@10.128.73.64/mjpg/video.mjpg")

def click(event, x, y, flags, param):

	if event == cv2.EVENT_LBUTTONDOWN:
		cv2.imwrite(os.path.join(path , f'{time.time()}_{x}{y}.jpg'), cap.read()[1])
  
cv2.namedWindow('frame')
cv2.setMouseCallback('frame',click)

while True:
    ret, frame = cap.read()
    print(frame.shape)
    # shown = cv2.resize(frame, (640, 480))
    
    cv2.imshow("frame", frame)
    
    cv2.waitKey(1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    