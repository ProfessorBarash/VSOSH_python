import cv2
from camera.camera import Camera
from camera.robot_detection import ZonesDetection
from robot.robot_control import Robot
from robot import robot_algorithms

camera = Camera("/dev/video0", 1, (1920, 1080))

x_target, y_target = 553, 449
robot = Robot()
zones_detector = ZonesDetection()

def mouse_callback(event, x, y, flags, param):
    global x_target, y_target
    if event == cv2.EVENT_LBUTTONDOWN:  # Если нажата ЛКМ
        print(f"ЛКМ нажата в точке: ({x}, {y})")
        x_target, y_target = x, y

cv2.namedWindow("main frame")
cv2.setMouseCallback("main frame", mouse_callback)

# M = cv2.moments(zones_detector.storage_zone[0])
# cx = int(M['m10']/M['m00'])
# cy = int(M['m01']/M['m00'])
# robot_algorithms.deliver_cargo(camera, robot, cx, cy, 3)
robot_algorithms.deliver_cargo(camera, robot, 117, 82, 3)

robot.robot_serial.send("l0")
robot.robot_serial.send("r0")
