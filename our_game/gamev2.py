import os
import random

import pygame as pg
from pygame.locals import *

window_width = 400
window_height = 680
BACKGROUND_COLOR = (78, 167, 187)
enemy_size = (30, 30)
SCORE = 0
player_shot_size = (17, 35)
screen_rect = Rect(0, 0, window_width, window_height)

game_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(file):
    file = os.path.join(game_dir, 'sprites', file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('image loading error')
    return surface.convert()


class Player(pg.sprite.Sprite):
    speed = 12
    images = []
    gun_offset = 8

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=screen_rect.midbottom)
        self.collideRect = pg.rect.Rect((0, 0), (12, 12))
        self.collideRect.midbottom = self.rect.midbottom

    def move(self, horiz_direction, vert_direction):
        self.rect.move_ip(horiz_direction * self.speed, vert_direction * self.speed)
        self.rect = self.rect.clamp(screen_rect)
        self.collideRect.move_ip(horiz_direction * self.speed, vert_direction * self.speed)
        self.collideRect = self.rect.clamp(screen_rect)

    def gun_pos(self, pos):
        return pos, self.rect.top


class Player_shot(pg.sprite.Sprite):
    speed = -15
    images = []
    GUN_RELOAD = 5

    def __init__(self, position):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midtop=position)
        self.image = pg.transform.scale(self.image, player_shot_size)
        self.collideRect = pg.rect.Rect((0, 0), (32, 32))
        self.collideRect.midbottom = self.rect.midbottom

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()


class Enemy(pg.sprite.Sprite):
    speed = 4
    images = []
    SPAWN_COOLDOWN = 4
    CROW_SOUND_COOLDOWN = 30

    def __init__(self):
        self.x = random.randrange(0, window_width, window_width // 10)
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(self.x, 0))
        self.image = pg.transform.scale(self.image, enemy_size)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top >= window_height:
            self.kill()


def load_sound(file):
    file = os.path.join(game_dir, 'sounds', file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print('Warning, unable to load, %s' % file)


class Score(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.SysFont('Comic Sans MS', 40)
        self.font.set_italic(1)
        self.color = Color('red')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(0, 0)

    def update(self):
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)


def main():
    pg.init()
    pg.font.init()
    screen = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption('My_game')
    clock = pg.time.Clock()

    # sprites
    img = load_image('player.png')
    Player.images = [img]
    img = load_image('player_shot.png')
    Player_shot.images = [img]
    img = load_image('enemy_new.png')
    Enemy.images = [img]

    # sounds
    crow_sound = load_sound('crow.wav')
    shot_sound = load_sound('shot.wav')
    shot_sound.set_volume(0.1)

    background = pg.Surface(screen_rect.size)
    background.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))

    pg.display.flip()

    # Создание контейнеров
    all = pg.sprite.RenderUpdates()
    shots = pg.sprite.Group()
    enemies = pg.sprite.Group()

    # Присвоение контейнеров
    Player.containers = all
    Player_shot.containers = all, shots
    Enemy.containers = all, enemies

    player = Player()
    # Таймеры появлений объектов
    gun_timer = 0
    enemy_spawn_timer = 0
    crow_sound_timer = 0
    game_over = False

    global SCORE

    if pg.font:
        all.add(Score())

    while player.alive():
        for event in pg.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return

        key_state = pg.key.get_pressed()
        horiz_direction = key_state[K_RIGHT] - key_state[K_LEFT]
        vert_direction = key_state[K_DOWN] - key_state[K_UP]
        player.move(horiz_direction, vert_direction)

        for shot in shots:
            enemies_hit_list = pg.sprite.spritecollide(shot, enemies, True)
            if len(enemies_hit_list) > 0:
                if crow_sound_timer <= 0:
                    crow_sound.play()
                    crow_sound_timer = Enemy.CROW_SOUND_COOLDOWN
                shot.kill()
                SCORE += len(enemies_hit_list)
        crow_sound_timer -= 1

        d = pg.sprite.spritecollide(player, enemies, True)
        if len(d) > 0:
            player.kill()
            game_over = True

        if key_state[K_x]:
            if gun_timer != 0:
                gun_timer = gun_timer - 1
            else:
                posL = player.rect.centerx - player.gun_offset + player_shot_size[0] / 2
                posR = player.rect.centerx + player.gun_offset + player_shot_size[0] / 2
                Player_shot(player.gun_pos(posL))
                Player_shot(player.gun_pos(posR))
                shot_sound.play()
                gun_timer = Player_shot.GUN_RELOAD

        if enemy_spawn_timer != 0:
            enemy_spawn_timer = enemy_spawn_timer - 1
        else:
            Enemy()
            enemy_spawn_timer = Enemy.SPAWN_COOLDOWN

        all.clear(screen, background)
        all.update()
        pg.display.update(all.draw(screen))
        clock.tick(60)

    while game_over:
        for event in pg.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
        pg.font.init()
        myfont = pg.font.SysFont('Comic Sans MS', 40)
        myfontbot = pg.font.SysFont('Comic Sans MS', 20)
        textover = myfont.render('Game over', False, (0, 0, 0))
        textscore = myfont.render('Score: ' + str(SCORE), False, (0, 0, 0))
        instruction = myfontbot.render('Press S to start a new game ', False, (0, 0, 0))

        key_state = pg.key.get_pressed()
        if key_state[K_s]:
            SCORE = 0
            main()
            return
        screen.blit(background, (0, 0))
        screen.blit(textover, (100, 0))
        screen.blit(textscore, (125, 100))
        screen.blit(instruction, (50, 600))
        pg.display.update()
        clock.tick(60)
    pg.quit()


if __name__ == '__main__': main()
