from camera.aruco import find_aruco_coords_and_angle
import cv2
import numpy as np
import pickle
from camera.aruco import draw_aruco_markers
from camera.big_box_contour import get_bix_box_cnt


class RobotDetector:
    def __init__(self, id):
        self.id = id
        
    def get_coord(self, frame):
        coords_and_angle = find_aruco_coords_and_angle(frame, self.id)
        if coords_and_angle is not None:
            return coords_and_angle[0]
        else:
            return None
    
    def get_angle(self, frame):
        coords_and_angle = find_aruco_coords_and_angle(frame, self.id)
        if coords_and_angle is not None:
            return coords_and_angle[1]
        else:
            return None
    

class ZonesDetection:
    def __init__(self, import_zone = (0, 0, 0), export_zone = (0, 0, 0), storage_zone = (0, 0, 0)):
        self.import_zone_low, self.import_zone_high, self.import_zone_count = import_zone
        self.export_zone_low, self.export_zone_high, self.export_zone_count = export_zone
        self.storage_zone_low, self.storage_zone_high, self.storage_zone_count = storage_zone
        
        try:
            zones_cash = open(f"zones_cash.p", "rb")

            self.storage_zone, self.import_zone, self.export_zone = pickle.load(zones_cash)
            self.is_cash = True
        except:
            self.is_cash = False
        
    def find_zone(self, frame, type):
        if type == "import":
            h_min, s_min, v_min = self.import_zone_low
            h_max, s_max, v_max = self.import_zone_high
            count = self.import_zone_count
        elif type == "export":
            h_min, s_min, v_min = self.export_zone_low
            h_max, s_max, v_max = self.export_zone_high
            count = self.export_zone_count
        else:
            h_min, s_min, v_min = self.storage_zone_low
            h_max, s_max, v_max = self.storage_zone_high
            count = self.storage_zone_count
            
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:count]
        
        return contours
    
    def create_cash(self, frame):
        storage_zone = self.find_zone(frame, "storage")
        import_zone = self.find_zone(frame, "import")
        export_zone = self.find_zone(frame, "export")
        
        file = open(f'../zones_cash.p', 'wb')
        pickle.dump((storage_zone, import_zone, export_zone), file)
        file.close()
        
    
    def debug_draw(self, frame, markers = False):
        
        original_frame = frame.copy()
        
        if self.is_cash:
            storage_zone = self.storage_zone
            import_zone = self.import_zone
            export_zone = self.export_zone
        else:
            storage_zone = self.find_zone(frame, "storage")
            import_zone = self.find_zone(frame, "import")
            export_zone = self.find_zone(frame, "export")
            
        
        
        cv2.drawContours(frame, storage_zone, -1, (0, 0, 0), 2)
        cv2.drawContours(frame, import_zone, -1, (0, 0, 255), 2)
        cv2.drawContours(frame, export_zone, -1, (255, 255, 0), 2)
        (x, y), angle = find_aruco_coords_and_angle(original_frame, 11)
        cv2.drawContours(frame, [get_bix_box_cnt(x, y, angle)], -1, (0, 255, 0), 2)
        cv2.circle(frame, find_aruco_coords_and_angle(original_frame, 2)[0], 20, (255, 0, 255), 5)
        
        if markers:
            draw_aruco_markers(original_frame, frame)
        
        return frame

