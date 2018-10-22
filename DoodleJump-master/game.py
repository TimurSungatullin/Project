import pygame
from pygame.sprite import collide_rect

from doodler import Doodler
from flying_platform import Platform
import random


class DoodleJump:
    pygame.init()
    pygame.display.set_caption("Doodle Jump")
    platforms = []  # координаты платформ

    def __init__(self):
        self.window = pygame.display.set_mode((700, 700))
        self.platforms = [[400, 700]]
        self.platform = pygame.image.load("static/platform_mini.png")
        self.doodler = Doodler()
        self.curr_level = 50
        self.run = True


    def draw_platforms(self):
        global a
        print(len(self.platforms))
        for platform in self.platforms:
            a = random.randint(0, 700)
            if platform[1] > self.doodler.cameray + 700:
                self.platforms.remove(platform)
            self.window.blit(self.platform, (platform[0], platform[1] - self.doodler.cameray))
        if self.platforms[-1][1] >= self.doodler.cameray:
            self.platforms.append([a, self.platforms[-1][1] - 50])
            self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 100])


    def update_platforms(self):
        player = pygame.Rect(self.doodler.x,
                             self.doodler.y,
                             self.doodler.image.get_width(),
                             self.doodler.image.get_height()-10)

        for platform in self.platforms:
            rect = pygame.Rect(platform[0], platform[1], self.platform.get_width(), self.platform.get_height())
            if rect.colliderect(player) and self.doodler.gravity and self.doodler.y < platform[1] - self.doodler.cameray:
                self.doodler.jump = 15
                self.doodler.gravity = 0

    def isDeath(self):
        if self.doodler.y - self.doodler.cameray > 1000:
            self.platforms = [[0, -100, 0]]
            self.run = False
            print("Умер")

    def main(self):
        # platform = Platform()

        while self.run:
            if self.doodler.y - self.doodler.cameray < 1000:
                self.update_platforms()
            self.draw_platforms()
            self.window.blit(self.doodler.image, [self.doodler.x, self.doodler.y - self.doodler.cameray])
            self.doodler.update()
            pygame.display.update()
            pygame.time.delay(30)
            self.window.fill((0, 220, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.isDeath()

    pygame.quit()


DoodleJump().main()
