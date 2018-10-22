import pygame, random, math

import Test
import Menu
import About

pygame.init()

tests = True
size = [800, 800]
width = 800
height = 800
screen = pygame.display.set_mode(size)
fon = pygame.image.load("pictures/fon.jpg")
clock = pygame.time.Clock()
chick = pygame.image.load('pictures/chick.png')
duck = pygame.image.load('pictures/duck.png')
parrot = pygame.image.load('pictures/parrot.png')


class load_sound():
    def __init__(self):
        self.sndBB = pygame.mixer.Sound('BB.wav')
        self.soundTik = pygame.mixer.Sound('Tik.wav')
        pygame.mixer.music.load("game_proc.mp3")


snd = load_sound()


def go_play():
    Menu.drow()
    while tests:
        if Menu.check == 1:
            start_game()
            Test.drow(scores)
        if Menu.check == 2:
            About.run = True
            About.drow()
        if About.flag:
            Menu.running = True
            Menu.drow()


class dulo():
    def __init__(self):
        self.startx = height / 2
        self.starty = width / 2
        self.wid = 5
        self.speed = 4
        self.length = 700
        self.ugol = 0
        self.endx = math.cos(math.radians(self.ugol)) * self.length + 400
        self.endy = math.sin(math.radians(self.ugol)) * self.length + 400


# класс движухщихся шариков
class balls():
    def __init__(self):
        self.radius = 30
        self.rect = chick.get_rect()
        check = random.randint(0, 2)
        if check == 0:
            self.color = (255, 0, 0)
        if check == 1:
            self.color = (0, 255, 0)
        if check == 2:
            self.color = (255, 255, 0)
        self.x = width - self.radius - 5
        self.y = self.radius + 5


# это класс шариков выстрелов
class my_ball():
    def __init__(self):
        choose_color = random.randint(0, 2)
        self.radius = 30
        self.x = 400
        self.y = 400
        self.ugol = 0
        self.speed = 13
        if choose_color == 0:
            self.color = (255, 0, 0)
        if choose_color == 1:
            self.color = (0, 255, 0)
        if choose_color == 2:
            self.color = (255, 255, 0)
        self.check = False


def start_game():
    speed = 5
    middle = 400
    CONST_100 = 100
    CONST_170 = 170
    count_of_balls = 0
    moving_balls = []
    x = 0
    y = 0
    running = True
    count_for_music = 0
    count_for_music = 0
    b = 0

    # функция по движению и рисованию шариков, которые движутся по периметру
    def drow_moving_balls():
        running = True
        for ball in moving_balls:
            if ball.x > ball.radius + speed + 5 and ball.y == ball.radius + 5:
                ball.x -= speed
            elif ball.y < width - ball.radius - 5 and ball.x == ball.radius + speed + 5:
                ball.y += speed
            elif ball.x < height - ball.radius - 5 and ball.y == width - ball.radius - 5:
                ball.x += speed
            elif ball.y > CONST_100 and ball.x == height - ball.radius - 5:
                ball.y -= speed
            elif ball.x > CONST_100 and ball.y == CONST_100:
                ball.x -= speed
            elif ball.y < width - CONST_100 and ball.x == CONST_100:
                ball.y += speed
            elif ball.x < height - CONST_100 and ball.y == width - CONST_100:
                ball.x += speed
            elif ball.y > CONST_170 and ball.x == height - CONST_100:
                ball.y -= speed
            elif ball.x > CONST_170 and ball.y == CONST_170:
                ball.x -= speed
            elif ball.y < width - CONST_170 and ball.x == CONST_170:
                ball.y += speed
            elif ball.x < height - CONST_170 and ball.y == width - CONST_170:
                ball.x += speed
            elif ball.y > middle and ball.x == height - CONST_170:
                ball.y -= speed
            elif ball.x > middle and ball.y == middle:
                ball.x -= speed
            elif ball.x - ball.radius < middle + ball.radius:
                snd.soundBB.play()
                running = False
                break
            if ball.color == (255, 0, 0):
                screen.blit(parrot, (normalize(ball.x), normalize(ball.y)))
            elif ball.color == (0, 255, 0):
                screen.blit(duck, (normalize(ball.x), normalize(ball.y)))
            else:
                screen.blit(chick, (normalize(ball.x), normalize(ball.y)))
        return running  # can delete

    def normalize(a):
        """
        why
        :param a:
        :return:
        """
        return a - 30

    pygame.mixer.music.play()
    next_ball = my_ball()
    current_ball = my_ball()
    shouting_balls = []
    d = dulo()
    global scores
    scores = 0

    while running:
        for event in pygame.event.get():
            # обработка пробела(выстрел)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # sound1.play()
                count_for_music += 1
                snd.soundTik.play()
                current_ball = next_ball
                current_ball.ugol = d.ugol
                next_ball = my_ball()
                current_ball.check = True
                shouting_balls.append(current_ball)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                global tests
                tests = False

        screen.blit(fon, (0, 0))
        pygame.draw.circle(screen, (255, 255, 255), (400, 400), (30))
        # pygame.draw.circle(screen, next_ball.color, (next_ball.x, next_ball.y), next_ball.r, 5)
        if next_ball.color == (255, 0, 0):
            screen.blit(parrot, (normalize(next_ball.x), normalize(next_ball.y)))
        elif next_ball.color == (0, 255, 0):
            screen.blit(duck, (normalize(next_ball.x), normalize(next_ball.y)))
        else:
            screen.blit(chick, (normalize(next_ball.x), normalize(next_ball.y)))
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            d.ugol += d.speed
            if d.ugol % 360 == 0:
                d.ugol = 0
            d.endx = math.cos(math.radians(d.ugol)) * d.length + 400
            d.endy = math.sin(math.radians(d.ugol)) * d.length + 400

        if keys[pygame.K_LEFT]:
            d.ugol -= d.speed
            if d.ugol % 360 == 0:
                d.ugol = 360
            d.endx = math.cos(math.radians(d.ugol)) * d.length + 400
            d.endy = math.sin(math.radians(d.ugol)) * d.length + 400

        pygame.draw.line(screen, (255, 0, 0), (d.startx, d.starty), (d.endx, d.endy), d.wid)

        # пробегаемся по массиву всех выстреленных шариков, чтоб изменить координаты
        for ball in shouting_balls:
            if ball.x < 800 and ball.x > 0 and ball.y > 0 and ball.y < 800 and ball.check:
                ball.x += math.cos(math.radians(ball.ugol)) * ball.speed
                ball.y += math.sin(math.radians(ball.ugol)) * ball.speed
                if ball.color == (255, 0, 0):
                    screen.blit(parrot, (normalize(int(ball.x)), normalize(int(ball.y))))
                elif ball.color == (0, 255, 0):
                    screen.blit(duck, (normalize(int(ball.x)), normalize(int(ball.y))))
                else:
                    screen.blit(chick, (normalize(int(ball.x)), normalize(int(ball.y))))
            else:
                ball.check = False
                shouting_balls.pop(shouting_balls.index(ball))
            for move_ball in moving_balls:
                if abs(ball.x - move_ball.x) < 30 and abs(ball.y - move_ball.y) < 30:
                    k = 1
                    if ball.color == move_ball.color:
                        k += 1
                        index1 = moving_balls.index(move_ball) - 1
                        index2 = index1 + 1
                        while moving_balls[index1].color == ball.color and len(moving_balls) - 1 > 0:
                            k += 1
                            moving_balls.pop(index1)
                            index1 -= 1
                            index2 -= 1
                        while moving_balls[index2].color == ball.color and len(moving_balls) > index2 + 1:
                            k += 1
                            moving_balls.pop(index2)

                        scores += 2 ** k
                    elif ball.color != move_ball.color:
                        scores -= 5
                    shouting_balls.pop(shouting_balls.index(ball))

        if count_of_balls % 13 == 0:
            moving_balls.append(balls())
        count_of_balls += 1

        if not drow_moving_balls():
            running = False

        pygame.display.flip()
        clock.tick(30)


go_play()
pygame.quit()
