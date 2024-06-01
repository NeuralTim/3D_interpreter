import re

class ReadOBJ():
    
    def read(self, path):
        triangles = []
        vertices = []
        with open(path, 'r') as obj_file:
            for line in obj_file:
                if line[0] == 'f':
                    triangles.append(list(map(int, re.findall(r'-?\d+\.?\d*', line))))
                elif line[0] == 'v':
                    vertices.append(list(map(float, re.findall(r'-?\d+\.?\d*', line))))
        
        return vertices, triangles