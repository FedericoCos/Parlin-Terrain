import pygame as pg
from pygame.locals import *
import sys
from Terrain import *
from math import sin, cos


# global variables
WIDTH = 600
HEIGHT = 600
FPS = 15
BLACK = (0, 0, 0)

T_W = 600
T_H = 700
SIZE = 10
ANGLE = 2.3
HEIGHT_TERR = 300
OFFSET = 0


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Terrain")
        self.clock = pg.time.Clock()
        self.surface = pg.display.get_surface()

        self.angle = ANGLE

        self.rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(self.angle), -sin(self.angle)],
            [0, sin(self.angle), cos(self.angle)],
        ]).astype(float)

        self.adder = 0

        self.terrain = Terrain(T_W // SIZE, T_H // SIZE, SIZE, HEIGHT_TERR)

    def game_loop(self):
        while True:
            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill(BLACK)
            self.terrain.draw(self.surface, self.rotation_x, self.adder, OFFSET)
            self.adder += 0.1

            pg.display.flip()


game = Game()
game.game_loop()
