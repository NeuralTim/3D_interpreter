import numpy as np

def generate_terrain(x_range, z_range):
    x_range = range(x_range)
    z_range = range(z_range)
    
    vertices = []
    y_prev = 0
    for x in x_range:
        for z in z_range:
            y = y_prev + np.random.uniform(-0.5, 0.5)
            vertices.append((x, y, z))
            y_prev = y


    triangles = []
    n = len(z_range)
    for x in range(len(x_range) - 1):
        for z in range(len(z_range) - 1):
            top_left = x * n + z
            top_right = top_left + 1
            bottom_left = (x + 1) * n + z
            bottom_right = bottom_left + 1
            
            triangles.append([top_left, bottom_left, bottom_right])  # CW
            triangles.append([top_left, bottom_right, top_right])    # CW

    return vertices, triangles