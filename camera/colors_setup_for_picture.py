import cv2
import numpy as np
import pickle


def nothing(x):
    return x


cv2.namedWindow('color setup')
cv2.createTrackbar('h_min','color setup',0,255,nothing)
cv2.createTrackbar('h_max','color setup',255,255,nothing)
cv2.createTrackbar('s_min','color setup',0,255,nothing)
cv2.createTrackbar('s_max','color setup',255,255,nothing)
cv2.createTrackbar('v_min','color setup',0,255,nothing)
cv2.createTrackbar('v_max','color setup',255,255,nothing)

def read(frame):
    params_file = open(f"/home/nto-pc/projects/IRS_final/params.p", "rb")

    params = pickle.load(params_file)

    mtx = params[1]
    dist = params[2]

    w, h = 1280, 800
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(params[1], params[2], (w, h), 1, (w, h))

    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    h,  w = frame.shape[:2]
    x, y, w, h = roi
    frame = dst[y:y+h, x:x+w]
    
    pts_src = np.array([[793, 42], [766, 614], [188, 613], [194, 28]], dtype=np.float32)

    pts_dst = np.array([[0, 0], [w//2, 0], [w//2, h], [0, h]], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

    frame = cv2.warpPerspective(frame, matrix, (w//2, h))
        
    return frame

cap = cv2.VideoCapture("http://root:admin@10.128.73.80/mjpg/video.mjpg")

blue_low = (100, 101, 155)
blue_high = (112, 255, 255)

red_low = (168, 43, 146)
red_high = (177, 162, 255)

white_low = (83, 14, 208)
white_high = (105, 69, 255)

while True:
    # frame = read(cv2.imread("/home/nto-pc/projects/IRS_final/graph/sample_image.jpg"))
    
    ret, frame = cap.read()
    
    # h_min = cv2.getTrackbarPos("h_min", 'color setup')
    # h_max = cv2.getTrackbarPos("h_max", 'color setup')
    # s_min = cv2.getTrackbarPos("s_min", 'color setup')
    # s_max = cv2.getTrackbarPos("s_max", 'color setup')
    # v_min = cv2.getTrackbarPos("v_min", 'color setup')
    # v_max = cv2.getTrackbarPos("v_max", 'color setup')
    h_min, s_min, v_min = white_low
    h_max, s_max, v_max = white_high

    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    
    cv2.drawContours(frame, contours[:7], -1, (0, 255, 0), 2)
    
    cv2.imshow('color setup', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        print(f"low = ({h_min}, {s_min}, {v_min})\nhigh = ({h_max}, {s_max}, {v_max})")
        break
    
