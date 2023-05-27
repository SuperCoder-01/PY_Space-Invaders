import pygame as pg

WIDTH, HEIGHT = 650, 650
WIN = pg.display.set_mode((WIDTH, HEIGHT))
FPS = 60

YellowShip = pg.image.load(r".\assets\yellow ship.png") # Player
YellowLaser = pg.image.load(r".\assets\yellow laser.png")
RedShip = pg.image.load(r".\assets\red ship.png")
RedLaser = pg.image.load(r".\assets\red laser.png")
GreenShip = pg.image.load(r".\assets\green ship.png")
GreenLaser = pg.image.load(r".\assets\green laser.png")
BlueShip = pg.image.load(r".\assets\blue ship.png")
BlueLaser = pg.image.load(r".\assets\blue laser.png")
BG = pg.transform.scale(pg.image.load(r".\assets\background.png"), (WIDTH, HEIGHT))