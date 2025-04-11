import cv2
from camera import Camera
from aruco import find_aruco_coords_and_angle
import numpy as np
import pickle

low = (47, 0, 189)
high = (135, 96, 255)



camera = Camera("http://root:admin@10.128.73.80/mjpg/video.mjpg", 1, (1280, 800))
camera.undistort = True


cv2.namedWindow("main frame")

while True:
    frame = camera.read()

    cv2.imshow("main frame", frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, low, high)
        
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for i in contours:
        frame_for_cnt = np.zeros_like(frame)
        (x, y), angle = find_aruco_coords_and_angle(frame, 11)
        cv2.drawContours(frame_for_cnt, [i], -1, (255, 255, 255), cv2.FILLED)
        
        file = open(f'big_box.p', 'wb')
        print("file opened")
        pickle.dump((i, (x, y), angle), file)
        file.close()
        print("file closed")
            
        cv2.imshow("big boy", frame_for_cnt)
        cv2.waitKey(0)

        

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break