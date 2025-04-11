import cv2
import numpy as np
import pickle
import math

low = (47, 0, 189)
high = (135, 96, 255)

params_file = open(f"big_box.p", "rb")

cnt, (x_old, y_old), angle_old = pickle.load(params_file)

def get_bix_box_cnt(x, y, angle):
    rotation_matrix = cv2.getRotationMatrix2D((x_old, y_old), math.degrees(angle - angle_old), 1.0)

    rotated_contour = cv2.transform(np.array(cnt), rotation_matrix).squeeze()
    
    dx = x - x_old
    dy = y - y_old
    translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])

    translated_contour = cv2.transform(np.array([rotated_contour]), translation_matrix).squeeze()

    return translated_contour