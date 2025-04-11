import cv2
import numpy as np
from camera.big_box_contour import get_bix_box_cnt

params = cv2.aruco.DetectorParameters()
dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(dictionary=dict, detectorParams=params)


aruco_dict = {0:"export", 
              1:"export",
              2:"robot",
              3:"cargo",
              4:"cargo",
              5:"cargo",
              6:"cargo",
              7:"cargo",
              8:"cargo",
              9:"cargo",
              10:"cargo",
              11:"big_cargo"}


def draw_aruco_markers(frame, res_frame = None, meaning = False):
    
    (corners, ids, rejected) = detector.detectMarkers(frame)
    
    if ids is not None:
        ids[ids == 17] = 8 #Aruco 17 is shit(he is detected because of camera low resolution)
    
    if res_frame is not None:
        cv2.aruco.drawDetectedMarkers(res_frame, corners, ids, (0, 255, 0))
        
        if meaning:
            for id in range(len(ids)):
                if id in aruco_dict.keys():
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.6
                    thickness = 2
                    x, y, _, _ = cv2.boundingRect(corners[id])
                    cv2.putText(res_frame, aruco_dict[ids[id][0]], (x + 20, y + 20), font, font_scale, (0, 0, 0), thickness)
        
        return res_frame
    else:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids, (0, 255, 0))
        return frame
        





def find_aruco_coords_and_angle(frame, id):
    (corners, ids, rejected) = detector.detectMarkers(frame)
    
    

    
    if ids is not None and id in ids:
        ids[ids == 17] = 8 #Aruco 17 is shit(he is detected because of camera low resolution)
        index = np.where(ids == id)[0][0]  
        corner = corners[index][0]
        
        top_left = corner[0]
        top_right = corner[1]
        bottom_right = corner[2]
        bottom_left = corner[3]

        center_x = int((top_left[0] + bottom_right[0]) / 2)
        center_y = int((top_left[1] + bottom_right[1]) / 2)
        center = (center_x, center_y)

        # Угол маркера
        angle = np.arctan2(top_right[1] - bottom_right[1], top_right[0] - bottom_right[0]) * -1

        return (center_x, center_y), angle
    else:
        return (0, 0), 0
    
def find_aruco_corner(frame, goal_cargo):

    (corners, ids, rejected) = detector.detectMarkers(frame)
    
    

    crnrs = []

    small_cargo_ids = [4, 5, 6, 7, 8, 9, 10, 11]
    if goal_cargo is not None:
        small_cargo_ids.remove(goal_cargo)

    if ids is not None:
        ids[ids == 17] = 8 #Aruco 17 is shit(he is detected because of camera low resolution)
        for currend_id in range(len(ids)):
            if ids[currend_id] in small_cargo_ids:
                crnrs.append(corners[currend_id])
                
    return crnrs

def increase_contour_size(contour, scale=1.05):
    """
    Увеличивает контур на заданный процент относительно его центра.

    :param contour: Контур, представленный как массив точек формы (N, 1, 2).
    :param scale: Коэффициент масштабирования (например, 1.05 для увеличения на 5%).
    :return: Увеличенный контур.
    """
    # Преобразуем контур в массив формы (N, 2)
    contour = np.array(contour, dtype=np.float32).reshape(-1, 2)
    
    # Находим центр масс контура
    M = cv2.moments(contour)
    if M["m00"] == 0:
        return contour.reshape(-1, 1, 2)  # Возвращаем контур в исходной форме
    
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    
    # Создаем матрицу для масштабирования
    scale_matrix = np.array([[scale, 0, (1 - scale) * cx],
                             [0, scale, (1 - scale) * cy]])
    
    # Применяем аффинное преобразование к контуру
    contour = cv2.transform(np.array([contour]), scale_matrix)
    
    # Возвращаем контур в форме (N, 1, 2)
    return contour.reshape(-1, 1, 2).astype(np.int32)

def increase_aruco_corners_size(corners, scale=1.05):
    """
    Увеличивает координаты углов ArUco маркера на заданный процент относительно центра маркера.

    :param corners: Список массивов углов, возвращаемый cv2.aruco.detectMarkers.
                   Каждый массив имеет форму (1, 4, 2).
    :param scale: Коэффициент масштабирования (например, 1.05 для увеличения на 5%).
    :return: Список массивов с увеличенными координатами углов.
    """
    enlarged_corners = []
    for marker_corners in corners:
        # Вычисляем центр маркера как среднее значение всех углов
        center = np.mean(marker_corners, axis=1)
        
        # Масштабируем углы относительно центра
        scaled_corners = (marker_corners - center) * scale + center
        
        enlarged_corners.append(scaled_corners)
    
    return enlarged_corners

    
def find_points(frame, goal_cargo=None, storage_zones=None):
    
    original_frame = frame.copy()

    mask = np.zeros_like(frame)

    corners = find_aruco_corner(frame, goal_cargo)

    contours = []

    if storage_zones is not None:
        for zone in storage_zones:
            if not is_aruco_in_contour(original_frame, zone):
                contours.append(zone)
    
    if goal_cargo != 11:
        (x, y), angle = find_aruco_coords_and_angle(frame, 11)
        big_box_contour = get_bix_box_cnt(x, y, angle)

        cv2.drawContours(mask, [increase_contour_size(big_box_contour, 1.5)], -1, (255, 255, 255), cv2.FILLED)
        
    # print(contours)
    
    cv2.drawContours(mask, contours, -1, (255, 255, 255), cv2.FILLED)

    

        
    kernel_size = (15, 15)  # You can adjust this size
    kernel = np.ones(kernel_size, np.uint8)

    # Perform dilation
    mask = cv2.dilate(mask, kernel, iterations=0)
    
    for corner in corners:
        center = np.mean(corner, axis=1)
        if list(mask[int(center[0][1]), int(center[0][0])]) == [255, 255, 255]:
            pass
        else:
            corner = increase_aruco_corners_size([corner], 2)[0]

        cv2.fillPoly(mask, np.int32(corner), (255, 255, 255))
    
    mask[0:24, :] = [255, 255, 255]  # Верхняя граница
    mask[-24:-1, :] = [255, 255, 255]  # Нижняя граница
    mask[-1, :] = [255, 255, 255]  # Нижняя граница
    mask[:, 0:24] = [255, 255, 255]  # Левая граница
    mask[:, -24:-1] = [255, 255, 255]  # Правая граница
    mask[:, -1] = [255, 255, 255]


    # mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    return 255 - mask

def is_aruco_in_contour(frame, cnt):
    
    mask = np.zeros_like(frame)
    cv2.drawContours(mask, [cnt], -1, (255, 255, 255), cv2.FILLED)
    
    frame = cv2.bitwise_and(frame, mask)
    
    (corners, ids, rejected) = detector.detectMarkers(frame)
    
    if ids is None:
        return True
    else:
        return False

def split_contour_and_find_centers(contour):
    # Аппроксимируем контур до прямоугольника
    rect = cv2.minAreaRect(contour)
    center, size, angle = rect

    # Находим ширину и высоту прямоугольника
    width, height = size
    if width < height:
        width, height = height, width  # width всегда больше height
        angle += 90  # Корректируем угол, если width и height поменялись местами

    # Разбиваем прямоугольник на 6 частей
    # 1 разрез на меньшей стороне (height), 2 на большей (width)
    x_step = width / 2  # Шаг по длинной стороне
    y_step = height / 1  # Шаг по короткой стороне

    # Создаем массив для центров масс
    centers = []

    # Вычисляем центры масс для каждой части
    for i in range(2):  # По длинной стороне
        for j in range(1):  # По короткой стороне
            # Локальные координаты центра масс
            local_x = (i + 0.5) * x_step - width / 2
            local_y = (j + 0.5) * y_step - height / 2

            # Поворачиваем координаты на угол прямоугольника
            theta = np.radians(angle)
            rotation_matrix = np.array([
                [np.cos(theta), -np.sin(theta)],
                [np.sin(theta), np.cos(theta)]
            ])
            rotated_point = np.dot(rotation_matrix, np.array([local_x, local_y]))

            # Сдвигаем координаты на центр прямоугольника
            global_x = int(center[0] + rotated_point[0])
            global_y = int(center[1] + rotated_point[1])

            centers.append((global_x, global_y))

    return centers