import cv2
from camera.camera import Camera
from camera.aruco import draw_aruco_markers, find_aruco_coords_and_angle
from robot.robot_control import Robot

camera = Camera("http://root:admin@10.128.73.80/mjpg/video.mjpg", 1, (1280, 800))
camera.undistort = True
# camera.start()

x_target, y_target = 0, 0
# robot = Robot(4, 15)

def mouse_callback(event, x, y, flags, param):
    global x_target, y_target
    if event == cv2.EVENT_LBUTTONDOWN:  # Если нажата ЛКМ
        print(f"ЛКМ нажата в точке: ({x}, {y})")
        x_target, y_target = x, y

cv2.namedWindow("main frame")
cv2.setMouseCallback("main frame", mouse_callback)

while True:
    
    frame = camera.read()


    # frame = draw_aruco_markers(frame)
    
    cv2.imshow("main frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break