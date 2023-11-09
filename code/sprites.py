import os
import pygame as pg
import math
import random
from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.imagen_path = os.path.join("graphics", "R_Base.png")
        self.image = pg.image.load(self.imagen_path)
        self.image = pg.transform.scale(self.image, (24, 48))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = vec(x, y)
        self.last_shot = 0
        self.last_shotS = 0
        self.health = PLAYER_HEALTH
        self.special = PLAYER_SPECIAL

    SPECIAL_REGEN_RATE = 10

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED

        if keys[pg.K_LCTRL]:
            self.vx *= 0.5
            self.vy *= 0.5

        if keys[pg.K_LSHIFT]:
            self.vx *= 2.0
            self.vy *= 2.0

        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shotS > BULLET_RATE:
                self.last_shotS = now
                self.bullets_attack()

        if self.special >= 1000:
            if keys[pg.K_z]:
                now = pg.time.get_ticks()
                if now - self.last_shot > SBULLET_RATE:
                    self.last_shot = now
                    self.special -= 1000
                    self.bullets_special()
            else:
                self.special += Player.SPECIAL_REGEN_RATE
        else:
            self.special += Player.SPECIAL_REGEN_RATE

        self.special = min(PLAYER_SPECIAL, self.special)

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
            self.pos = vec(self.x, self.y)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def bullets_attack(self):
        attack = pg.mixer.Sound(os.path.join('audio', 'damage00.wav'))
        attack.set_volume(0.3)
        pg.mixer.Sound.play(attack)

        bullet1 = BulletCard(self.game, self.pos)
        bullet2 = BulletCard(self.game, self.pos + vec(24, 0))

    def bullets_special(self):
        special = pg.mixer.Sound(os.path.join('audio', 'power1.wav'))
        special.set_volume(0.3)
        pg.mixer.Sound.play(special)

        bulletA = BulletSpecial(self.game, self.pos + vec(-35, 22))
        bulletB = BulletSpecial(self.game, self.pos + vec(60, 22))
        bulletC = BulletSpecial(self.game, self.pos + vec(12, 70))
        bulletD = BulletSpecial(self.game, self.pos + vec(12, -25))

        bulletA = BulletSpecialMini(self.game, self.pos + vec(-35, -25))
        bulletB = BulletSpecialMini(self.game, self.pos + vec(60, -25))
        bulletC = BulletSpecialMini(self.game, self.pos + vec(-35, 70))
        bulletD = BulletSpecialMini(self.game, self.pos + vec(60, 70))

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.x = int(self.x)
        self.y = int(self.y)
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.pos = vec(self.x, self.y)


class BulletCard(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        bulletc_path = os.path.join("graphics", "R_Shots_A.png")
        self.image = pg.image.load(bulletc_path)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, -BULLET_SPEED)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if self.rect.bottom < 0:
            self.kill()


class BulletSpecial(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites)
        self.game = game

        self.colors = ["R_Special_RA.png", "R_Special_GA.png", "R_Special_BA.png"]
        color_index = random.randint(0, 2)
        bullets_path = os.path.join("graphics", self.colors[color_index])

        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (48, 48))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, -SBULLET_SPEED)
        self.spawn_time = pg.time.get_ticks()
        self.delay = 500

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.delay:
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos

            if self.pos.y <= 0:
                bounce = pg.mixer.Sound(os.path.join('audio', 'tan00.wav'))
                pg.mixer.Sound.play(bounce)
                bounce.set_volume(0.1)
                self.vel.y = SBULLET_SPEED

            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos

            if self.rect.top > HEIGHT:
                self.kill()


class BulletSpecialMini(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites)
        self.game = game

        self.colors = ["R_Special_RB.png", "R_Special_GB.png", "R_Special_BB.png"]
        color_index = random.randint(0, 2)
        bullets_path = os.path.join("graphics", self.colors[color_index])

        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (32, 32))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, -SBULLET_SPEED)
        self.spawn_time = pg.time.get_ticks()
        self.delay = 500

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.delay:
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos
            self.rect.center = (self.pos.x, self.pos.y)


class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.imagen_path = os.path.join("graphics", "K_Base.png")
        self.image = pg.image.load(self.imagen_path)
        self.image = pg.transform.scale(self.image, (38, 54))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = vec(self.x, self.y)

    def get_position(self):
        return self.pos

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.pos = vec(self.x, self.y)


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE