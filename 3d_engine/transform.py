import numpy as np
from math import sin, cos

class Transform():
    def __init__(self) -> None:
        pass

    def rot_x(self, point, angle):
        self.x_matrix = [[1, 0, 0], 
                         [0, cos(angle), -sin(angle)],
                         [0, sin(angle), cos(angle)]]
        return np.matmul(point, self.x_matrix)

    def rot_y(self, point, angle):
        self.y_matrix = [[cos(angle), 0, sin(angle)], 
                         [0, 1, 0], 
                         [-sin(angle), 0, cos(angle)]]
        return np.matmul(point, self.y_matrix)

    def rot_z(self, point, angle):
        self.z_matrix = [[cos(angle), -sin(angle), 0],
                         [sin(angle), cos(angle), 0],
                         [0, 0, 1]]
        return np.matmul(point, self.z_matrix)
    
    def translate(self, point, vector):
        if len(point) == len(vector):
            new_point = []
            for i in range(len(point)):
                new_point.append(point[i] + vector[i])
            return new_point
        else:
            print("lenghts of point and vector doesn't match")
            return None