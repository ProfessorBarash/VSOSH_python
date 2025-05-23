import math
import time
from robot.PID import PID_regulator
from camera.robot_detection import RobotDetector
import bluetooth

class Robot:
    def __init__(self, marker_id: int = 2, bd_addr: str = "5C:01:3B:96:8C:22" ) -> None:
        self.robot_detection = RobotDetector(marker_id)
        self.robot_serial = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.robot_serial.connect((bd_addr, 1))
        print("Подключено")
        self.angle_PID = PID_regulator(50, 0, 0)
        self.distance_PID = PID_regulator(0.5, 0.00003, 2)

    def distance(self, point1: tuple[int, int], point2: tuple[int, int]) -> float:
        if point1 is None or point2 is None:
            return None
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    
    def normalise_angle(self, angle):
        if angle > math.pi:
            angle -= 2 * math.pi
        elif angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def compute_wheel_speed(self, v: float, omega: float) -> tuple[float, float]:
        min_val = 45
        omega_r = v + omega
        if abs(omega_r) < min_val:
            omega_r = min_val * (omega_r / abs(omega_r))
        omega_l = v - omega
        if abs(omega_l) < min_val:
            omega_l = min_val * (omega_l / abs(omega_l))
        return omega_l, omega_r

    def move_to_point(self, frame, target_point: tuple[int, int], on_one_position = False) -> None:
        robot_center = self.robot_detection.get_coord(frame)
        robot_angle = self.robot_detection.get_angle(frame)
        
        if robot_center is None or robot_angle is None:
            return False
        
        angle_error = (math.atan2(target_point[1] - robot_center[1], target_point[0] - robot_center[0]) * -1) - robot_angle
        angle_error = self.normalise_angle(angle_error)
        
        distance_error = self.distance(robot_center, target_point)
        
        if distance_error < 20 and not on_one_position:
            self.robot_serial.send("l0")
            self.robot_serial.send("r0")
            self.angle_PID.clear_PID()
            self.distance_PID.clear_PID()
            return True
        
        if on_one_position and abs(math.degrees(angle_error)) < 30:
            self.robot_serial.send("l0")
            self.robot_serial.send("r0")
            self.angle_PID.clear_PID()
            self.distance_PID.clear_PID()
            return True
            
        v = self.distance_PID.compute_PID(distance_error)
        omega = self.angle_PID.compute_PID(angle_error)
        
        if abs(math.degrees(angle_error)) > 30 or on_one_position:
            v = 0

        omega_l, omega_r = self.compute_wheel_speed(v, omega)

        self.robot_serial.send(f"l{int(omega_l)}")
        self.robot_serial.send(f"r{int(omega_r)}")
        
        return False