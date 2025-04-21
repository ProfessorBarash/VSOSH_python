from robot.robot_control import Robot
from camera.camera import Camera
import cv2
import math
from graph.graph import Graph
from camera.aruco import find_aruco_coords_and_angle, find_points

def pass_graph(camera: Camera, robot: Robot, path, cargo_id: int|None = None):
    death_zone = 20
    frame = camera.read()
    while not robot.move_to_point(frame, path[0]):
        frame = camera.read()
        cv2.circle(frame, tuple(map(int, path[0])), 2, (0, 255, 0), -1)
        cv2.imshow("main frame", frame)
        if cargo_id is not None:
            if robot.distance(find_aruco_coords_and_angle(frame, cargo_id)[0], path[-1]) < death_zone:
                return True
        if cv2.waitKey(1) & 0xFF == ord('q'):
            robot.robot_serial.send("l0")
            robot.robot_serial.send("r0")
            break

    for point in range(0, len(path), 20):
        while not robot.move_to_point(frame, path[point]):
            frame = camera.read()
            if cargo_id is not None:
                if robot.distance(find_aruco_coords_and_angle(frame, cargo_id)[0], path[point]) > 40:
                    return False
                if robot.distance(find_aruco_coords_and_angle(frame, cargo_id)[0], path[-1]) < death_zone:
                    return True
            cv2.circle(frame, tuple(map(int, path[point])), 2, (0, 255, 0), -1)
            cv2.imshow("main frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                robot.robot_serial.send("l0")
                robot.robot_serial.send("r0")
                break

    while not robot.move_to_point(frame, path[-1]):
        frame = camera.read()
        cv2.circle(frame, tuple(map(int, path[-1])), 2, (0, 255, 0), -1)
        cv2.imshow("main frame", frame)
        if cargo_id is not None:
            if robot.distance(find_aruco_coords_and_angle(frame, cargo_id)[0], path[-1]) < death_zone:
                return True
        if cv2.waitKey(1) & 0xFF == ord('q'):
            robot.robot_serial.send("l0")
            robot.robot_serial.send("r0")
            break
    if cargo_id is not None:
        if robot.distance(find_aruco_coords_and_angle(frame, cargo_id)[0], path[-1]) < death_zone:
            return True
    return False


def behind_cargo(point0, point1, line_len, mask):
    try:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    except:
        pass
        
    angle = math.atan2(point1[1] - point0[1], point1[0] - point0[0])
    
    for i in range(line_len, 0, -1):
        x_offset = i * math.cos(angle) 
        y_offset = i * math.sin(angle) 
        if mask[int(point0[1] - y_offset), int(point0[0] - x_offset)]:
            return int(point0[0] - x_offset), int(point0[1] - y_offset)
        
    x_offset = line_len * math.cos(angle) 
    y_offset = line_len * math.sin(angle) 
    return int(point0[0] - x_offset), int(point0[1] - y_offset)


def deliver_cargo(camera, robot, x_target, y_target, cargo_id):
    first_try = True
    while True:
        frame = camera.read()

        mask = find_points(frame, cargo_id)
        graph = Graph(mask, False)

        cv2.imshow("main frame", frame)

        robot.robot_serial.send("l0")
        robot.robot_serial.send("r0")

        cv2.waitKey(1)

        path = graph.find_path(find_aruco_coords_and_angle(frame, cargo_id)[0], (x_target, y_target))
        path = graph.approximation(path)

        mask = find_points(frame)
        graph = Graph(mask)
        robot_path = graph.find_path(robot.robot_detection.get_coord(frame), behind_cargo(path[0], path[10], 80, mask))
        if robot_path[-1][1] < 0 or robot_path[-1][1] > frame.shape[0] or\
            robot_path[-1][0] < 0 or robot_path[-1][0] > frame.shape[1]:
            continue

        if robot.distance(robot.robot_detection.get_coord(frame), robot_path[-1]) < \
            robot.distance(robot.robot_detection.get_coord(frame), find_aruco_coords_and_angle(frame, cargo_id)[0]) and \
            not first_try:
            pass_graph(camera, robot, [robot_path[-1]])
        else:
            pass_graph(camera, robot, robot_path)

        if pass_graph(camera, robot, path, cargo_id):
            break
        else:
            robot.robot_serial.send("l-100")
            robot.robot_serial.send("r-100")
            cv2.waitKey(500)
            robot.robot_serial.send("l0")
            robot.robot_serial.send("r0")

        first_try = False

    robot.robot_serial.send("l-100")
    robot.robot_serial.send("r-100")
    cv2.waitKey(500)
    robot.robot_serial.send("l0")
    robot.robot_serial.send("r0")
