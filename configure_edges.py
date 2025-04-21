import cv2
from camera.camera import Camera
from camera.aruco import draw_aruco_markers, find_aruco_coords_and_angle
from robot.robot_control import Robot

camera = Camera("/dev/video0", 1, (1920, 1080))

def mouse_callback(event, x, y, flags, param):
    global x_target, y_target
    if event == cv2.EVENT_LBUTTONDOWN:  # Если нажата ЛКМ
        print(f"ЛКМ нажата в точке: ({x}, {y})")

cv2.namedWindow("main frame")
cv2.setMouseCallback("main frame", mouse_callback)

while True:
    
    frame = camera.read()
    
    cv2.imshow("main frame", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break