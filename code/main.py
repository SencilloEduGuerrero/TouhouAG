import pygame as pg
import sys, os
from sprites import *
from settings import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.background = pg.transform.scale(BACKGROUND, (528, 816))
        self.background_position = 0
        self.music_path = os.path.join("audio", "TouhouBossMusic.mp3")
        pg.mixer.music.load(self.music_path)
        pg.mixer.music.play(2)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row in range(17):
            Wall(self, -1, row)
            Wall(self, 11, row)
            if row < 17:
                Wall(self, row, 17)
                Wall(self, row, -1)
        self.player = Player(self, 252, 722)
        self.boss = Boss(self, 245, 48)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range (0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range (0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption(GAME_NAME + " FPS:({:.0f})".format(self.clock.get_fps()))
        self.background_position += 1

        if self.background_position >= self.background.get_height():
            self.background_position = 0

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, self.background_position - self.background.get_height()))
        self.screen.blit(self.background, (0, self.background_position))

        self.draw_grid()
        self.all_sprites.draw(self.screen)

        pg.display.flip()
        self.clock.tick(60)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()
