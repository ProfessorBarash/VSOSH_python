import cv2
from collections import deque
import numpy as np
import heapq

class Graph:
    def __init__(self, image, show_graph = False):
        self.graph = {}

        image = image.astype("uint8")

        image = cv2.ximgproc.thinning(cv2.split(image)[0])
        
        if show_graph:
            cv2.imshow("mat", image)
            cv2.waitKey(0)

        height, width = image.shape[:2]
        offset = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        for y in range(height):
            for x in range(width):
                if image[y, x]:
                    self.graph[(x, y)] = []
                    for x_offset, y_offset in offset:
                        try:
                            if image[y + y_offset, x + x_offset]:
                                self.graph[(x, y)].append((x + x_offset, y + y_offset))
                        except:
                            continue

    def nearest(self, point):
        min_distance = float('inf')
        min_point = None

        for x, y in self.graph.keys():
            distance = (point[0] - x) ** 2 + (point[1] - y) ** 2
            if min_distance > distance:
                min_point = (x, y)
                min_distance = distance

        return min_point
    
    def find_path(self, start_point, finish_point):
        start = self.nearest(start_point)
        finish = self.nearest(finish_point)
        queue = deque()
        queue.append([start])
        visited = set()

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == finish:
                return [start_point] + path + [finish_point]
            
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.get(node, []):
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        return None

    def generate_line(self, point0, point1, num_points):
        point0 = np.array(point0)
        point1 = np.array(point1)

        t = np.linspace(0, 1, num_points)

        points = point0 + t[:, np.newaxis] * (point1 - point0)

        return points.tolist()

    def approximation(self, path):
        updated_path = [path[0]]
        for i in range(70, len(path), 70):
            updated_path += self.generate_line(updated_path[-1], path[i], 70) 

        updated_path += self.generate_line(updated_path[-1], path[-1], 70)

        return updated_path
