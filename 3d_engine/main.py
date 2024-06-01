import pygame as pg
import numpy as np
from math import tan, acos
from transform import Transform
from operations import Tools
from read_obj import ReadOBJ
import get_sphere
import get_terrain
Transform = Transform()
Tools = Tools()
ReadOBJ = ReadOBJ()

pg.init()
clock = pg.time.Clock()
dim = 600
screen = pg.display.set_mode((dim, dim))
camera_pos = [0, 0, -1]

vertices, tri = ReadOBJ.read('tinker.obj')
triangles = []
for a in tri:
    v = []
    for b in a:
        v.append(b-1)
    triangles.append(v)
    


vertices = [[0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1], 
            [0, 1, 1]]

triangles = [
    [0, 1, 2],  # Front face
    [0, 2, 3],  # Front face
    [1, 5, 6],  # Right face
    [1, 6, 2],  # Right face
    [5, 4, 7],  # Back face
    [5, 7, 6],  # Back face
    [4, 0, 3],  # Left face
    [4, 3, 7],  # Left face
    [3, 2, 6],  # Top face
    [3, 6, 7],  # Top face
    [4, 5, 1],  # Bottom face
    [4, 1, 0]   # Bottom face
]


vertices1, triangles1 = get_sphere.generate_sphere_vertices_and_triangles(1, 10)
vertices, triangles = get_terrain.generate_terrain(13, 13)

 # in CW order

class Camera():
    def __init__(self, pos, rotations, movement_vector, render_distance, min_render_distance, FOV) -> None:
        self.pos = pos
        self.rotations = rotations
        self.vector = movement_vector
        self.render_distance = render_distance
        self.min_dist = min_render_distance
        self.FOV = FOV
    


class Object():
    def __init__(self, vert, tri, camera, my_starting_pos_relative_to_origin) -> None:    # it's going to be splited into classes Object and Camera
        self.vert = vert
        self.tri = tri
        self.render_distance = camera.render_distance
        self.min_dist = camera.min_dist
        self.FOV = camera.FOV
        self.camera_pos = camera.pos
        self.translating_vector = camera.vector
        self.rotations = camera.rotations
        self.current_angles = [0, 0, 0]
        self.camera_pointing_vector = [0, 0, -1]
        self.my_starting_pos_relative_to_origin = my_starting_pos_relative_to_origin
        self.z_buffer = []

    def visibility_test(self, triangle):
        for v in triangle:
            d = Tools.dist(self.camera_pos, v)
            if d > self.min_dist and d < self.render_distance:
                pass
            else:
                return False
            
        v1 = Tools.vector(triangle[1], triangle[0])
        v2 = Tools.vector(triangle[1], triangle[2])
        c_p = np.cross(v1, v2)
        c_p /= np.linalg.norm(c_p)

        cam_to_c_p_vec = Tools.vector(triangle[2], self.camera_pos)
        cam_to_c_p_vec /= np.linalg.norm(cam_to_c_p_vec)

        self.angle_between_c_p_and_cam_v = np.dot(c_p, cam_to_c_p_vec)
        if self.angle_between_c_p_and_cam_v < 0 and np.degrees(acos(np.dot(self.camera_pointing_vector, cam_to_c_p_vec))) < self.FOV/2:
            return True
        return False
    
    def apply_perspective(self, point):
        tg = tan(np.radians(self.FOV/2))
        return [(1/tg)*point[0]/point[2], (1/tg)*point[1]/point[2]]

    def normalize(self, values):
        new_values = []
        for new_value in values:
            new_value = (new_value+1)/2
            new_value = int(dim*new_value)
            new_values.append(new_value)
        return new_values
    
    def rotate(self, angles, v):
        v = Transform.rot_x(v, angles[0])
        v = Transform.rot_y(v, angles[1])
        v = Transform.rot_z(v, angles[2])
        return v


    def move_by_vector(self, point, vector):
        return np.add(point, vector)


    def return_visible_transformed_rotated_triangles(self):
        tri_moved_and_rotated = []

        for t in self.tri:
            self.vert_a = self.move_by_vector(self.vert[t[0]], self.my_starting_pos_relative_to_origin)
            self.vert_b = self.move_by_vector(self.vert[t[1]], self.my_starting_pos_relative_to_origin)
            self.vert_c = self.move_by_vector(self.vert[t[2]], self.my_starting_pos_relative_to_origin)
            self.vert_a = self.move_by_vector(self.vert_a, self.translating_vector)
            self.vert_b = self.move_by_vector(self.vert_b, self.translating_vector)
            self.vert_c = self.move_by_vector(self.vert_c, self.translating_vector)
            self.vert_a = self.rotate(self.rotations, self.vert_a)
            self.vert_b = self.rotate(self.rotations, self.vert_b)
            self.vert_c = self.rotate(self.rotations, self.vert_c)
            tri_moved_and_rotated.append([self.vert_a, self.vert_b, self.vert_c])

        this_object_moved_rotated_visile_tris = []
        for tri in tri_moved_and_rotated:
            if self.visibility_test(tri):
                a = self.normalize(self.apply_perspective(tri[0]))
                b = self.normalize(self.apply_perspective(tri[1]))
                c = self.normalize(self.apply_perspective(tri[2]))
                avarage_z = tri[0][2] + tri[0][2] + tri[0][2]
                color = -int(self.angle_between_c_p_and_cam_v*255)
                color = [color, color, color]
                this_object_moved_rotated_visile_tris.append([a, b, c, avarage_z, color])
        return this_object_moved_rotated_visile_tris


    def get_hitbox(self):
        pass


run = True
Camera = Camera(camera_pos, [0.0, 0.0, 0.0], [0, 0, -7], 50, 1, 90)
Object0 = Object(vertices, triangles, Camera, [0, 0, 0])
Object1 = Object(vertices1, triangles1, Camera, [1, 1.5, 0])
list_of_objects = [Object1]
ang = 0
while run:
    FPS = clock.get_fps()
    print(FPS)
    clock.tick()
    screen.fill((0, 0, 0))
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            pg.quit()
            run = False
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        Camera.vector[2] -= 0.4
    if keys[pg.K_s]:
        Camera.vector[2] += 0.4
    if keys[pg.K_a]:
        Camera.vector[0] += 0.4
    if keys[pg.K_d]:
        Camera.vector[0] -= 0.4
    if keys[pg.K_o]:
        Camera.vector[1] -= 0.4
    if keys[pg.K_l]:
        Camera.vector[1] += 0.4

    if keys[pg.K_UP]:
        Camera.rotations[0] -= 0.03
    if keys[pg.K_DOWN]:
        Camera.rotations[0] += 0.03
    if keys[pg.K_LEFT]:
        Camera.rotations[1] += 0.03
    if keys[pg.K_RIGHT]:
        Camera.rotations[1] -= 0.03
    if keys[pg.K_z]:
        Camera.rotations[2] -= 0.03
    if keys[pg.K_x]:
        Camera.rotations[2] += 0.03

    scene = []
    for obj in list_of_objects:
        scene.extend(obj.return_visible_transformed_rotated_triangles())
    
    scene = sorted(scene, key=lambda z: z[2])
    scene.reverse()
    for triangle in scene:
        pg.draw.polygon(screen, triangle[4], (triangle[0], triangle[1], triangle[2]))
    
    pg.display.flip()
