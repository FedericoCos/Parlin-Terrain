import pygame as pg
import numpy as np
import numba
import random
import perlin_noise

WHITE = (255, 255, 255)
RED = (255, 0, 0)

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
]).astype(float)


@numba.jit(nopython=True)
def projection(rot, point):
    app_rot = np.dot(rot, point.reshape((3, 1)))

    return np.dot(projection_matrix, app_rot)


@numba.jit(nopython=True)
def get_points(rotation, terrain, i, j, size, y_mult):
    project = projection(rotation, terrain[i, j])
    px = int(project[0][0]) + size * i
    py = int(project[1][0]) + y_mult

    p_dx = projection(rotation, terrain[i + 1, j])
    px_dx = int(p_dx[0][0]) + size * (i + 1)
    py_dx = int(p_dx[1][0]) + y_mult

    p_dw = projection(rotation, terrain[i, j - 1])
    px_dw = int(p_dw[0][0]) + size * i
    py_dw = int(p_dw[1][0]) + y_mult

    return px, py, px_dx, py_dx, px_dw, py_dw


class Terrain:
    def __init__(self, x_axis, y_axis, size, terr_height):
        self.terrain = np.zeros((x_axis, y_axis, 3))
        self.size = size

        self.rows = x_axis
        self.cols = y_axis

        self.y_mult = self.cols * self.size

        self.perlin = perlin_noise.PerlinNoise(octaves=1.5, seed=random.randint(1, 100))
        self.terr_height = terr_height
        self.step = 0.08

        y_off = 0
        for y in range(y_axis):
            x_off = 0
            for x in range(x_axis):
                z_rand = self.perlin.noise([x_off, y_off]) * self.terr_height
                self.terrain[x, y] = np.matrix([x * size + size / 2, y * size + size / 2, z_rand])
                x_off += self.step
            y_off += self.step

    def draw(self, surface, rotation, adder, offset):
        for j in range(1, self.cols):
            for i in range(self.rows - 1):
                px, py, px_dx, py_dx, px_dw, py_dw = get_points(rotation, self.terrain, i, j, self.size, self.y_mult)
                py += offset
                py_dw += offset
                py_dx += offset

                pg.draw.line(surface, WHITE, (px, py), (px_dw, py_dw))
                pg.draw.line(surface, WHITE, (px, py), (px_dx, py_dx))
                pg.draw.line(surface, WHITE, (px_dw, py_dw), (px_dx, py_dx))

        y_off = adder
        for j in range(self.cols):
            x_off = 0
            for i in range(self.rows):
                self.terrain[i, j, 2] = self.perlin.noise([x_off, y_off]) * self.terr_height
                x_off += self.step
            y_off += self.step
