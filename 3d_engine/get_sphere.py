import numpy as np

def generate_sphere_vertices_and_triangles(radius, subdivisions):
    vertices = []
    triangles = []

    # Generate vertices
    for i in range(subdivisions + 1):
        theta = i * np.pi / subdivisions  # from 0 to pi
        for j in range(subdivisions + 1):
            phi = j * 2 * np.pi / subdivisions  # from 0 to 2pi
            x = radius * np.sin(theta) * np.cos(phi)
            y = radius * np.sin(theta) * np.sin(phi)
            z = radius * np.cos(theta)
            vertices.append([x, y, z])

    # Generate triangles
    for i in range(subdivisions):
        for j in range(subdivisions):
            p1 = i * (subdivisions + 1) + j
            p2 = p1 + 1
            p3 = p1 + (subdivisions + 1)
            p4 = p3 + 1
            
            if i != 0:
                triangles.append([p1, p2, p3])
            if i != subdivisions - 1:
                triangles.append([p2, p4, p3])
    
    return vertices, triangles