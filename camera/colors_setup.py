import cv2
import numpy as np


def nothing(x):
    return x


cv2.namedWindow('color setup')
cv2.createTrackbar('h_min','color setup',0,255,nothing)
cv2.createTrackbar('h_max','color setup',255,255,nothing)
cv2.createTrackbar('s_min','color setup',0,255,nothing)
cv2.createTrackbar('s_max','color setup',255,255,nothing)
cv2.createTrackbar('v_min','color setup',0,255,nothing)
cv2.createTrackbar('v_max','color setup',255,255,nothing)

cap = cv2.VideoCapture("http://root:admin@10.128.73.80/mjpg/video.mjpg")
cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 127)
cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, 127)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) # auto mode
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
cap.set(cv2.CAP_PROP_EXPOSURE, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


ret, frame = cap.read()



# while True:
#     ret, frame = cap.read()
    
#     hue = cv2.getTrackbarPos("Hue", 'color setup')
#     hue_thresh = cv2.getTrackbarPos("Hue Threshhold", 'color setup')
#     saturation = cv2.getTrackbarPos("Saturation", 'color setup')
#     saturation_thresh = cv2.getTrackbarPos("Saturation Threshhold", 'color setup')
#     value = cv2.getTrackbarPos("Value", 'color setup')
#     value_thresh = cv2.getTrackbarPos("Value Threshhold", 'color setup')
    
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
#     mask = cv2.inRange(frame, (hue - hue_thresh, saturation - saturation_thresh, value - value_thresh), (hue + hue_thresh, saturation + saturation_thresh, value + value_thresh))
    
#     frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    
#     masked = cv2.bitwise_and(frame, frame, mask=mask)
    
#     cv2.imshow('color setup', masked)
#     if cv2.waitKey(30) & 0xFF == ord('q'):
#             break
    

while True:
    ret, frame = cap.read()
    
    h_min = cv2.getTrackbarPos("h_min", 'color setup')
    h_max = cv2.getTrackbarPos("h_max", 'color setup')
    s_min = cv2.getTrackbarPos("s_min", 'color setup')
    s_max = cv2.getTrackbarPos("s_max", 'color setup')
    v_min = cv2.getTrackbarPos("v_min", 'color setup')
    v_max = cv2.getTrackbarPos("v_max", 'color setup')

    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(frame, (h_min, s_min, v_min), (h_max, s_max, v_max))
    
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    
    masked = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.imshow('color setup', masked)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        print(f"low = ({h_min}, {s_min}, {v_min})\nhigh = ({h_max}, {s_max}, {v_max})")
        break
    
