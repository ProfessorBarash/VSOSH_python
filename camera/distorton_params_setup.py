import numpy as np
import cv2
import glob
import pickle

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

objpoints = [] 
imgpoints = [] 
images = glob.glob('/home/barash/projects/VSOSH_python/camera/samples/*')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (8,6), None)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        cv2.drawChessboardCorners(img, (8,6), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(30)
cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

params = (ret, mtx, dist, rvecs, tvecs)

file = open(f'params.p', 'wb')
pickle.dump(params, file)
file.close()

print(ret, mtx, dist, rvecs, tvecs, sep='\n'+'\n'+'\n')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
while True:
    ret, frame = cap.read()
    h,  w = frame.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    x, y, w, h = roi
    
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    
    cv2.imshow("dst", dst)
    
    if cv2.waitKey(30) == ord("q"):
        break