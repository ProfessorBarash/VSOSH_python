import cv2
from camera.camera import Camera
from camera.robot_detection import ZonesDetection

camera = Camera("http://root:admin@10.128.73.80/mjpg/video.mjpg", 1, (1280, 800))
camera.undistort = True

blue_low = (100, 101, 155)
blue_high = (112, 255, 255)

red_low = (168, 43, 146)
red_high = (177, 162, 255)

white_low = (81, 16, 215)
white_high = (113, 77, 255)

zones_detector = ZonesDetection((blue_low, blue_high, 1), (red_low, red_high, 2), (white_low, white_high, 7))

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Если нажата ЛКМ
        print(f"ЛКМ нажата в точке: ({x}, {y})")
        zones_detector.create_cash(param)

cv2.namedWindow("main frame")

while True:
    frame = camera.read()
    
    cv2.setMouseCallback("main frame", mouse_callback, frame)
    
    frame = zones_detector.debug_draw(frame, False)

    cv2.imshow("main frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break