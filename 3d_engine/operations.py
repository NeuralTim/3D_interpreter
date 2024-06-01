import numpy as np
from math import sin, cos, sqrt

class Tools():
    def __init__(self) -> None:
        pass

    def cross_product(self, vec1, vec2):
        if len(vec1) == 3 and len(vec2) == 3:
            return [vec1[1]*vec2[2] - vec1[2]*vec2[1], vec1[2]*vec2[0] - vec1[0]*vec2[2], vec1[0]*vec2[1] - vec1[1]*vec2[0]]
        else:
            print("Sizes of vectors doesn't match")
            return None 
    
    def dist(self, P1, P2):
        if len(P1) == len(P2):
            d = 0
            for i, j in zip(P1, P2):
                d += abs(i - j)**2
            return sqrt(d)
        else:
            print("Sizes of vectors doesn't match")
            return None
        
    def vector(self, point1, point2):
        return np.subtract(point1, point2)