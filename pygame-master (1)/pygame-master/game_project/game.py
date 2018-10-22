import pygame as pg
import random as rnd

pg.init()

# globals
global screen, main_surface, fps, score, font
global entities, room_width, room_height, win_coef, spawn_count

font = pg.font.SysFont("courier", 16)
score = 0
room_width = 320
room_height = 240
win_coef = 2.5
screen = pg.display.set_mode((round(room_width * win_coef),
                              round(room_height * win_coef)))
main_surface = pg.Surface((room_width, room_height))
fps = 60
entities = pg.sprite.Group()
spawn_count = 5

clock = pg.time.Clock()
pg.display.set_caption("")
running = True


def load_sprite_strip(sprite, amount):
    sprite_strip = []
    for i in range(amount):
        sprite_strip.append(pg.image.load(sprite.format(i + 1)))
    return sprite_strip


# load background
spr_background = load_sprite_strip("sprites/bg/bg_{}.png", 6)
bg_anim = 0
bg_anim_speed = 0.1

# player sprites
spr_player_attack = load_sprite_strip("sprites/player/player_attack_{}.png", 5)
spr_player_fall = load_sprite_strip("sprites/player/player_fall_{}.png", 2)
spr_player_idle = load_sprite_strip("sprites/player/player_idle_{}.png", 4)
spr_player_jump = load_sprite_strip("sprites/player/player_jump_{}.png", 2)
spr_player_run = load_sprite_strip("sprites/player/player_run_{}.png", 4)

# entities
spr_ball_blue = load_sprite_strip("sprites/entities/ball_blue_{}.png", 4)
spr_ball_green = load_sprite_strip("sprites/entities/ball_green_{}.png", 4)
spr_ball_purple = load_sprite_strip("sprites/entities/ball_purple_{}.png", 4)
spr_ball_red = load_sprite_strip("sprites/entities/ball_red_{}.png", 4)

# other sprites
spr_ball_explosion = load_sprite_strip(
    "sprites/other/ball_explosion_{}.png", 3)


# extend this to draw entity
# extends pygame.sprite.Sprite
class Drawable(pg.sprite.Sprite):

    def __init__(self, x=0, y=0, image_index=0, image_speed=0,
                 sprite=[], origin_x=0, origin_y=0):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image_index = image_index
        self.image_speed = image_speed
        self.sprite = sprite
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.rect = sprite[0].get_rect()

    def update(self):
        self.rect.x = self.x - self.origin_x
        self.rect.y = self.y - self.origin_y

    def draw_rect(self, surface):
        pg.draw.rect(surface, (255, 0, 0),
                     pg.Rect(self.rect.x, self.rect.y,
                             self.rect.width, self.rect.height))

    def draw_self(self, surface):
        if len(self.sprite) > 0:
            if self.image_index >= len(self.sprite) - 1:
                self.image_index = 0;
            self.image_index += self.image_speed
            surface.blit(self.sprite[round(self.image_index)],
                         (self.x - self.origin_x, self.y - self.origin_y))


class Ball(Drawable):

    # call this instead of kill() to create explosion
    def explode(self):
        entities.add(Explosion(self.x, self.y, 0, 0.1,
                               spr_ball_explosion, spr_ball_explosion[0].get_width() // 2,
                               spr_ball_explosion[0].get_height() // 2))
        self.kill()


class Explosion(Drawable):

    # destroys itself after animation
    def draw_self(self, surface):
        if self.image_index >= len(self.sprite) - 1:
            self.kill()
        self.image_index += self.image_speed
        surface.blit(self.sprite[round(self.image_index)],
                     (self.x - self.origin_x, self.y - self.origin_y))


class Player(Drawable):

    def __init__(self, x=0, y=0, image_index=0, image_speed=0,
                 sprite=[], origin_x=0, origin_y=0, speed=2):
        Drawable.__init__(self, x, y, image_index, image_speed,
                          sprite, origin_x, origin_y)
        self.speed = speed
        self.right = False
        self.in_air = False
        self.jump_count = 56
        self.attack = False

    # to change animation sprites (jump, fall, idle etc.)
    def set_sprite(self, sprite):
        self.sprite = sprite
        self.rect = sprite[0].get_rect()

    # to change animation speed
    def set_image_speed(self, image_speed):
        self.image_speed = image_speed

    # change sprite direction
    def draw_self(self, surface):
        if self.image_index + self.image_speed >= len(self.sprite) - 1:
            self.image_index = 0
        self.image_index += self.image_speed
        if not self.right:
            surface.blit(self.sprite[round(self.image_index)],
                         (self.x - self.origin_x, self.y - self.origin_y))
        else:
            surface.blit(pg.transform.flip(self.sprite[round(self.image_index)],
                                           True, False), (self.x - self.origin_x, self.y - self.origin_y))


# generate stars
def generate_stars(amount):
    stars = pg.sprite.Group()
    for i in range(amount):
        x = rnd.randint(8, 312)
        y = rnd.randint(8, 100)
        sprite = rnd.choice([spr_ball_blue, spr_ball_red,
                             spr_ball_green, spr_ball_purple])
        image_index = rnd.randint(0, len(sprite) - 1)
        ball = Ball(x, y, image_index, 0.1, sprite,
                    sprite[0].get_width() // 2, sprite[0].get_height() // 2)
        entities.add(ball)
        stars.add(ball)
    return stars


stars = generate_stars(spawn_count)
player = Player(room_width // 2, room_height, 0, 0.05,
                spr_player_idle, 30, 64, 2)
entities.add(player)


def colide(player, stars, score):
    # hits = pg.sprite.spritecollide(player, stars, False)
    for star in stars:
        if (star.rect.center[0] - player.rect.center[0]) ** 2 + (star.rect.center[1] - player.rect.center[1]) ** 2 <= (player.rect.size[0] // 2) ** 2:
            star.explode()
            score += 1
    return score



# main game loop
while running:
    clock.tick(fps)

    # player actions
    # move player
    keys = pg.key.get_pressed()
    if not player.attack:
        player.set_sprite(spr_player_idle)
        player.set_image_speed(0.05)
    if keys[pg.K_LEFT] and player.x > 10:
        player.right = False
        player.x -= player.speed
        if not player.attack:
            player.set_sprite(spr_player_run)
            player.set_image_speed(0.1)
    if keys[pg.K_RIGHT] and player.x < room_width - 10:
        player.right = True
        player.x += player.speed
        if not player.attack:
            player.set_sprite(spr_player_run)
            player.set_image_speed(0.1)
    if not player.in_air:
        if keys[pg.K_UP]:
            player.in_air = True
    else:
        if player.jump_count >= -56:
            player.y -= player.jump_count / 8
            player.jump_count -= 1
            if player.jump_count < 0 and not player.attack:
                player.set_sprite(spr_player_fall)
                player.set_image_speed(0.1)
            elif player.jump_count >= 0 and not player.attack:
                player.set_sprite(spr_player_jump)
                player.set_image_speed(0.1)
        else:
            player.in_air = False
            player.jump_count = 56

    if player.attack:
        if round(player.image_index) == 2:
            score = colide(player, stars, score)
            if not stars.sprites():
                spawn_count += 5
                stars = generate_stars(spawn_count)

        if player.image_index >= 3.9:
            player.attack = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE and not player.attack and player.jump_count > 0:
                player.attack = True
                player.image_index = 0
                player.set_sprite(spr_player_attack)
                player.set_image_speed(0.1)

    # draw background
    if bg_anim >= len(spr_background) - 1:
        bg_anim = 0
    bg_anim += bg_anim_speed
    main_surface.blit(spr_background[round(bg_anim)], (0, 0))

    # draw entities
    if entities:
        for entity in entities:
            entity.update()
            # entity.draw_rect(main_surface)
            entity.draw_self(main_surface)

    if score >= 50 and score < 100:
        message = "Aren't you tired yet? "
    elif score >= 100:
        message = "Please, stop it((( "
    else:
        message = "Score: "
    main_surface.blit(font.render(message + score.__str__(), False, (255, 255, 255)), (0, 0))
    screen.blit(pg.transform.scale(main_surface,
                                   (round(room_width * win_coef), round(room_height * win_coef))), (0, 0))
    pg.display.flip()
pg.quit()
