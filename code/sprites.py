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
        self.vel = vec(0, 0)
        self.last_move_time = pg.time.get_ticks()
        self.move_interval = random.randint(1000, 3000)
        self.target_x = 0
        self.target_y = 0
        self.first_step = False
        self.health = BOSS_HEALTH
        self.phase = PHASE
        self.last_shot = 0
        self.bullet_spiral_timer = 0
        self.next_bullet_spiral_time = self.get_next_bullet_spiral_time()

    @staticmethod
    def get_next_bullet_spiral_time():
        return pg.time.get_ticks() + random.randint(MIN_BULLET_INTERVAL, MAX_BULLET_INTERVAL)

    def set_new_move_interval(self):
        self.move_interval = random.randint(MIN_MOVE_INTERVAL, MAX_MOVE_INTERVAL)
        self.target_x = random.randint(0, WIDTH_GAME - self.rect.width)
        self.target_y = random.randint(48, HEIGHT / 4 - self.rect.height)

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.last_move_time

        if current_time >= self.next_bullet_spiral_time:
            self.boss_bullets_attack()
            self.next_bullet_spiral_time = self.get_next_bullet_spiral_time()

        if elapsed_time >= self.move_interval:
            self.set_new_move_interval()
            self.last_move_time = current_time
            if not self.first_step:
                self.first_step = True

        else:
            self.move_interval = random.randint(4000, 8000)

        if self.first_step:
            interp_factor = 0.1
            self.pos.x = pg.math.lerp(self.pos.x, self.target_x, interp_factor)
            self.pos.y = pg.math.lerp(self.pos.y, self.target_y, interp_factor)

            self.pos.x = max(0, min(int(self.pos.x), WIDTH_GAME - self.rect.width))
            self.pos.y = max(48, min(int(self.pos.y), HEIGHT / 4 - self.rect.height))

            self.rect.topleft = int(self.pos.x), int(self.pos.y)
        else:
            interp_factor = 0.1
            self.pos.x = pg.math.lerp(self.pos.x, self.target_x, interp_factor)
            self.pos.y = pg.math.lerp(self.pos.y, self.target_y, interp_factor)

            self.pos.x = max(245, min(int(self.pos.x), WIDTH_GAME - self.rect.width))
            self.pos.y = max(96, min(int(self.pos.y), HEIGHT / 4 - self.rect.height))

            self.rect.topleft = self.pos.x, self.pos.y

    def boss_bullets_attack(self):
        attack = pg.mixer.Sound(os.path.join('audio', 'graze.wav'))
        attack.set_volume(0.05)
        pg.mixer.Sound.play(attack)

        bullet1 = BulletSpiral(self.game, self.rect.center)
        self.game.bullets.add(bullet1)


class BulletSpiral(pg.sprite.Sprite):
    def __init__(self, game, boss_pos):
        super().__init__()
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        bulletb_path = os.path.join("graphics", "K_Shots_A.png")
        self.image = pg.image.load(bulletb_path)
        self.rect = self.image.get_rect()
        self.pos = vec(boss_pos)
        self.rect.center = boss_pos
        self.angle = 0
        self.radius = 2
        self.angular_speed = 2
        self.lifetime = B_BULLET_LIFETIME
        self.speed = B_BULLET_SPEED

    def update(self):
        self.angle += self.angular_speed * self.game.dt

        self.pos.x = self.rect.centerx + math.cos(self.angle) * self.radius
        self.pos.y = self.rect.centery + math.sin(self.angle) * self.radius

        self.pos.y += self.speed * self.game.dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if self.rect.top < 0:
            self.kill()


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
