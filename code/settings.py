import pygame as pg
import os

WIDTH = 816
HEIGHT = 816
FPS = 60
TILESIZE = 48

GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WHITE = (250, 250, 250)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BLACK = (0, 0, 0)

GAME_NAME = 'Touhou Algorithm Genetic'

imagen_path = os.path.join("graphics", "background.png")
BACKGROUND = pg.image.load(imagen_path)
BACKGROUND = pg.transform.scale(BACKGROUND, (528, 816))

PLAYER_SPEED = 400

BULLET_SPEED = 1000
BULLET_RATE = 100
SBULLET_SPEED = 500
SBULLET_LIFETIME = 1000
