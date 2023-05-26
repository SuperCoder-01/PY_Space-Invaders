import pygame as pg
import random

pg.font.init()
Width, Height = 650, 650
WIN = pg.display.set_mode((Width, Height))
pg.display.set_caption("Space Invaders")

YellowShip = pg.image.load("assets/yellow ship.png") # Player
YellowLaser = pg.image.load("assets/yellow laser.png")
RedShip = pg.image.load("assets/red ship.png")
RedLaser = pg.image.load("assets/red laser.png")
GreenShip = pg.image.load("assets/green ship.png")
GreenLaser = pg.image.load("assets/green laser.png")
BlueShip = pg.image.load("assets/blue ship.png")
BlueLaser = pg.image.load("assets/blue laser.png")
BG = pg.transform.scale(pg.image.load("assets/background.png"), (Width, Height))

# Objects
class Laser:
    """Laser for enemy and player"""

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pg.mask.from_surface(self.img)

    def draw(self, window: pg.Surface):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel: int):
        self.y += vel

    def off_screen(self, height: int) -> bool:
        return self.y > height or self.y < 0

    def collision(self, obj: object) -> bool:
        return collide(self, obj)

class Ship:
    """Base class 'Ship'"""

    Cooldown = 15

    def __init__(self, x: int, y: int, health=100):
        self.x: int = x
        self.y: int = y
        self.health: int = health
        self.ship_img = None
        self.laser_img = None
        self.lasers: list[Laser] = []
        self.laserDelay: int = 0

    def draw(self, window: pg.Surface):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel: int, obj: object):
        self.coolDown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(Height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def coolDown(self):
        if self.laserDelay >= self.Cooldown:
            self.laserDelay = 0
        elif self.laserDelay > 0:
            self.laserDelay += 1

    def shoot(self):
        if self.laserDelay == 0:
            laser = Laser(self.x - 18, self.y, self.laser_img)
            self.lasers.append(laser)
            self.laserDelay = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    """Player class"""

    def __init__(self, x: int, y: int, health=100):
        super().__init__(x, y, health)
        self.ship_img = YellowShip
        self.laser_img = YellowLaser
        self.mask = pg.mask.from_surface(self.ship_img)
        self.max_health: int = health

    def move_lasers(self, vel: int, objs: list[object]):
        self.coolDown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(Height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window: pg.Surface):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window: pg.Surface):
        pg.draw.rect(window, (255, 0, 0), (self.x, self.y +
                         self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pg.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() +
                         10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    """Enemy ship inherited from base class Ship"""

    COLOR_MAP: dict[str, tuple[pg.Surface, pg.Surface]] = {
        "red": (RedShip, RedLaser),
        "green": (GreenShip, GreenLaser),
        "blue": (BlueShip, BlueLaser)
    }

    def __init__(self, x: int, y: int, color: str, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pg.mask.from_surface(self.ship_img)

    def move(self, vel: int):
        self.y += vel

    def shoot(self):
        if self.laserDelay == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.laserDelay = 1


def collide(obj1: object, obj2: object) -> bool:
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 3
    main_font = pg.font.SysFont("comicsans", 36)
    lost_font = pg.font.SysFont("comicsans", 36)
    enemies: list[Enemy] = []
    wave_length = 3
    enemy_vel = 1
    player_vel = 4
    laser_vel = 5
    player = Player(300, 550)
    clock = pg.time.Clock()
    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        lives_label = main_font.render(f"Lives: {lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", True, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (Width - level_label.get_width() - 10, 10))
        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)
        if lost:
            lost_label = lost_font.render("You Lost!!", True, (255, 255, 255))
            WIN.blit(lost_label, (Width / 2 - lost_label.get_width() / 2, 350))
        pg.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        if not enemies:
            level += 1
            wave_length += 5
            if player.health > 0:
                player.health += 10
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(50, Width - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))

                enemies.append(enemy)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pg.K_RIGHT] and player.x + player_vel + player.get_width() < Width:
            player.x += player_vel
        if keys[pg.K_SPACE]:
            player.shoot()
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 120) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > Height:
                lives -= 1
                enemies.remove(enemy)
        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pg.font.SysFont("arial", 48)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", True, (255, 255, 255))
        WIN.blit(title_label, (Width/2 - title_label.get_width()/2, 350))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                main()
    pg.quit()

main_menu()