import os, pygame, random
from pygame.locals import *
from Spaceship import Spaceship
from Asteroid import Asteroid


class Game:
    screen_height = 400
    screen_width = 600
    game_name = "Asteroids"
    x_coord = 5
    y_coord = screen_height / 2

    x_speed = 0
    y_speed = 0

    score = 1000  # стартовое количество очков жизни
    total_score = 0

    shag = 0  # счетчик, определяющий изменение направления движения астероидов

    go1 = 0  # сдвиги астероидов по вертикали
    go2 = 0
    go3 = 0

    def init_window(self):
        pygame.init()
        pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Asteroids')

    @staticmethod
    def load_image(name, color_key=None):  # отображение картинок
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        image = image.convert()
        if color_key is not None:
            if color_key is -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, RLEACCEL)
        return image, image.get_rect()

    def draw_background(self):
        screen = pygame.display.get_surface()
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        back, back_rect = self.load_image("space.jpg")
        screen.blit(back, (0, 0))
        pygame.display.flip()
        return back

    def input(self, events):  # задействование клавиш для передвижения космического корабля
        for event in events:
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x_speed = -1
                if event.key == pygame.K_RIGHT:
                    self.x_speed = 1
                if event.key == pygame.K_UP:
                    self.y_speed = -1
                if event.key == pygame.K_DOWN:
                    self.y_speed = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.x_speed = 0
                if event.key == pygame.K_RIGHT:
                    self.x_speed = 0
                if event.key == pygame.K_UP:
                    self.y_speed = 0
                if event.key == pygame.K_DOWN:
                    self.y_speed = 0
        self.x_coord = self.x_coord + self.x_speed
        self.y_coord = self.y_coord + self.y_speed
        if self.x_coord < 0:
            self.x_coord = 0
        if self.x_coord > self.screen_width - 50:
            self.x_coord = self.screen_width - 50
        if self.y_coord < 50:
            self.y_coord = 50
        if self.y_coord > self.screen_height - 50:
            self.y_coord = self.screen_height - 50

    def action(self, bk):
        screen = pygame.display.get_surface()
        s = Spaceship(1, 320)
        asteroid = Asteroid(500, 100)
        asteroid2 = Asteroid(800, 200)
        asteroid3 = Asteroid(1200, 350)
        asterow = [asteroid, asteroid2, asteroid3]
        air = [s]
        asteroids = pygame.sprite.RenderPlain(asterow)
        ss = pygame.sprite.RenderPlain(air)
        timer = pygame.time.Clock()
        while 1:
            timer.tick(600)
            if self.input(pygame.event.get()) == 1:
                return 1, -1
            blocks_hit_list = pygame.sprite.spritecollide(s, asteroids, False)
            if len(blocks_hit_list) > 0:
                self.score -= len(blocks_hit_list)
                asteroids.draw(screen)
                ss.draw(screen)
                if self.score < 1:
                    return 3, self.total_score // 100

            s.rect.x = self.x_coord
            s.rect.y = self.y_coord
            asteroid.rect.x = asteroid.rect.x - 1
            asteroid2.rect.x = asteroid2.rect.x - 1
            asteroid3.rect.x = asteroid3.rect.x - 1
            if asteroid.rect.x < 0:
                asteroid.rect.x = 500
                asteroid.rect.y = 100
            if asteroid2.rect.x < 0:
                asteroid2.rect.x = 800
                asteroid2.rect.y = 200
            if asteroid3.rect.x < 0:
                asteroid3.rect.x = 1200
                asteroid3.rect.y = 350
            if self.shag > 300:
                # self.shag = 0
                self.go1 = random.randint(-1, 1)
                self.go2 = random.randint(-1, 1)
                self.go3 = random.randint(-1, 1)
            asteroid.rect.y += self.go1
            asteroid2.rect.y += self.go2
            asteroid3.rect.y += self.go3
            self.shag += 1
            screen.blit(bk, (0, 0))
            font = pygame.font.SysFont('Comic Sans MS', 25)
            white = (255, 255, 255)
            life = int(self.score / 10)
            text = font.render("Health: " + str(life), True, white)
            screen.blit(text, [10, 10])
            text = font.render("Score: " + str(self.total_score // 100), 1, white)
            screen.blit(text, (475, 10))
            asteroids.update()
            ss.update()
            asteroids.draw(screen)
            ss.draw(screen)
            pygame.display.flip()
            self.total_score += timer.get_time()

    def main(self):
        self.init_window()
        bk = self. draw_background()
        return self. action(bk)
