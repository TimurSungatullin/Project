# <editor-fold desc="Основа">
import pygame
import time
import random
import datetime

from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
size = [600, 400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Eggs Game")
# </editor-fold>

# <editor-fold desc="Переменные">
flag_space_return = True
running = True
xCoord = [75.0, 515.0]
yCoord = [95.0, 150.0]
fromUpper = False
x = 0.0
y = 0.0
instructions = True
wolfIsTopRight = False
wolfIsTopLeft = True
wolfIsBottomRight = False
wolfIsBottomLeft = False
isFirstTime = True
menuFirstTime = True
currentScore = 0
currentLifes = 3
white = (255, 255, 255)
black = (0, 0, 0)
eggColor = (255, 255, 204)
brown = (210, 105, 30)
eggs = pygame.sprite.Group()
timer = time.clock()
fontBig = pygame.font.SysFont('Comic Sans MS', 35)
fontSmall = pygame.font.SysFont('Comic Sans MS', 20)
fontSuperSmall = pygame.font.SysFont('Comic Sans MS', 15)
fontMedium = pygame.font.SysFont('Comic Sans MS', 25)
inBag = False
toastyTime = False
toastyClockStart = 200
timer = time.clock()

# картинки
chicken1 = pygame.transform.scale(pygame.image.load('images/chicken1.png').convert_alpha(), (69, 71))
chicken2 = pygame.transform.scale(pygame.image.load('images/chicken2.png').convert_alpha(), (69, 71))
left_top_wolf = pygame.transform.scale(pygame.image.load('images/left_top_wolf.png').convert_alpha(), (133, 204))
right_top_wolf = pygame.transform.scale(pygame.image.load('images/right_top_wolf.png').convert_alpha(), (133, 204))
left_bottom_wolf = pygame.transform.scale(pygame.image.load('images/left_bottom_wolf.png').convert_alpha(), (133, 204))
right_bottom_wolf = pygame.transform.scale(pygame.image.load('images/right_bottom_wolf.png').convert_alpha(),
                                           (133, 204))
grass = pygame.transform.scale(pygame.image.load('images/grass.png').convert_alpha(), (600, 130))
wood1 = pygame.image.load('images/wood1.png')
wood2 = pygame.image.load('images/wood2.png')
wood3 = pygame.transform.rotate(pygame.image.load('images/wood3.png'), 80)
wood3_2 = pygame.transform.rotate(pygame.image.load('images/wood3_2.png'), 280)
sky = pygame.image.load('images/sky.png')

# звуковые эффекты
beep = pygame.mixer.Sound('sounds/beep.ogg')
game_over = pygame.mixer.Sound('sounds/game_over.wav')
egg_cracking = pygame.mixer.Sound('sounds/egg_cracking.wav')
egg_caught = pygame.mixer.Sound('sounds/egg_caught.ogg')
toasty = pygame.mixer.Sound('sounds/toasty.wav')
beep.set_volume(0.4)
game_over.set_volume(1.0)
egg_cracking.set_volume(0.2)
egg_caught.set_volume(0.2)
toasty.set_volume(1.0)


# </editor-fold>

# <editor-fold desc="Функции">
def AddEggs(eggs):
    egg = Egg(eggColor, 30, 40)
    egg.rect.x = random.choice(xCoord)
    egg.rect.y = random.choice(yCoord)
    egg.xc = egg.rect.x
    egg.yc = egg.rect.y
    eggs.add(egg)


def DrawWolfWhereNeeded():
    if wolfIsTopLeft:
        screen.blit(left_top_wolf, (222, 130))
    if wolfIsTopRight:
        screen.blit(right_top_wolf, (245, 130))
    if wolfIsBottomLeft:
        screen.blit(left_bottom_wolf, (222, 130))
    if wolfIsBottomRight:
        screen.blit(right_bottom_wolf, (245, 130))


def DrawBackgroundInGame():
    screen.blit(sky, (0, 0))
    screen.blit(grass, (0, 270))
    screen.blit(wood1, (0, 75))
    screen.blit(wood1, (525, 75))
    screen.blit(wood2, (0, 120))
    screen.blit(wood2, (0, 180))
    screen.blit(wood2, (525, 120))
    screen.blit(wood2, (525, 180))
    screen.blit(wood3, (67, 120))
    screen.blit(wood3, (67, 180))
    screen.blit(wood3_2, (385, 120))
    screen.blit(wood3_2, (385, 180))
    fontBerlin30 = pygame.font.SysFont('Berlin Sans FB', 30)
    score = fontMedium.render('Score: ' + str(currentScore), True, white)
    lifes = fontMedium.render('Lifes: ' + str(currentLifes), True, white)
    screen.blit(chicken1, (5, 70))  # верхняя левая курица
    screen.blit(chicken1, (5, 130))  # нижняя левая курица
    screen.blit(chicken2, (525, 70))  # верхняя правая курица
    screen.blit(chicken2, (525, 130))  # нижняя правая курица
    screen.blit(score, [445, 10])  # Score
    screen.blit(lifes, [445, 40])  # Lifes
    screen.blit(grass, (0, 270))


def DrawLines(color1, color2, color3):
    pygame.draw.line(screen, color1, (140, 208), (190, 208), 3)  # играть
    pygame.draw.line(screen, color1, (411, 208), (461, 208), 3)  # играть
    pygame.draw.line(screen, color2, (140, 258), (190, 258), 3)  # об игре
    pygame.draw.line(screen, color2, (411, 258), (461, 258), 3)  # об игре
    pygame.draw.line(screen, color3, (140, 308), (190, 308), 3)  # рекорды
    pygame.draw.line(screen, color3, (411, 308), (461, 308), 3)  # рекорды


def MakeStartMenu():
    global running, menuFirstTime
    if menuFirstTime:
        pygame.mixer.music.load('songs/metal.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, 0.0)
        menuFirstTime = False
    onPlayButton = True
    onAboutButton = False
    onRecordsButton = False
    screen.fill(black)
    pygame.draw.rect(screen, (240, 230, 140), ((100, 40), (400, 15)))
    pygame.draw.rect(screen, (240, 230, 140), ((100, 40), (15, 100)))
    pygame.draw.rect(screen, (240, 230, 140), ((100, 125), (400, 15)))
    pygame.draw.rect(screen, (240, 230, 140), ((485, 40), (15, 100)))
    pygame.draw.line(screen, white, (140, 208), (190, 208), 3)  # играть
    pygame.draw.line(screen, white, (411, 208), (461, 208), 3)  # играть
    pygame.draw.line(screen, white, (10, 10), (590, 10), 3)
    pygame.draw.line(screen, white, (10, 10), (10, 390), 3)
    pygame.draw.line(screen, white, (10, 390), (590, 390), 3)
    pygame.draw.line(screen, white, (590, 10), (590, 390), 3)
    screen.blit(fontBig.render('волк ловит яйца', True, brown), (124, 75))
    screen.blit(fontSmall.render('играть', True, brown), (258, 200))
    screen.blit(fontSmall.render('правила', True, brown), (250, 250))
    screen.blit(fontSmall.render('рекорды', True, brown), (248, 300))
    screen.blit(fontSuperSmall.render('2018', True, brown), (282, 370))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
        # <editor-fold desc="Обработка нажатия клавиш">
        pressedList = pygame.key.get_pressed()
        if pressedList[pygame.K_UP]:
            if onAboutButton:
                beep.play()
                if flag_up:
                    DrawLines(white, black, black)
                    onPlayButton = True
                    onAboutButton = False
                    onRecordsButton = False
                    pygame.display.flip()
                flag_up = False
            if onRecordsButton:
                beep.play()
                if flag_up:
                    DrawLines(black, white, black)
                    onPlayButton = False
                    onAboutButton = True
                    onRecordsButton = False
                    pygame.display.flip()
                flag_up = False
        else:
            flag_up = True

        if pressedList[pygame.K_DOWN]:
            if onPlayButton:
                beep.play()
                if flag_down:
                    DrawLines(black, white, black)
                    onPlayButton = False
                    onAboutButton = True
                    onRecordsButton = False
                    pygame.display.flip()
                flag_down = False
            if onAboutButton:
                beep.play()
                if flag_down:
                    DrawLines(black, black, white)
                    onPlayButton = False
                    onAboutButton = False
                    onRecordsButton = True
                    pygame.display.flip()
                flag_down = False
        else:
            flag_down = True

        if pressedList[pygame.K_SPACE] or pressedList[pygame.K_RETURN]:
            if flag_space_return:
                if onPlayButton:
                    beep.play()
                    pygame.mixer.music.load('songs/ofuzake.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1, 0.0)
                    time.sleep(0.3)
                    return
                if onAboutButton:
                    beep.play()
                    screen.fill(black)
                    MakeAboutMenu()
                    break
                if onRecordsButton:
                    beep.play()
                    screen.fill(black)
                    MakeRecordsMenu()
                    break
            flag_space_return = False
        else:
            flag_space_return = True
        # </editor-fold>


def MakeAboutMenu():
    global running, isFirstTime
    pygame.draw.line(screen, white, (10, 10), (590, 10), 3)
    pygame.draw.line(screen, white, (10, 10), (10, 390), 3)
    pygame.draw.line(screen, white, (10, 390), (590, 390), 3)
    pygame.draw.line(screen, white, (590, 10), (590, 390), 3)
    screen.blit(fontBig.render('правила', True, brown), (215, 75))
    file = open("instructions.txt")
    z = 120
    lines = file.read().split(r'\n')
    for line in lines:
        z += 18
        screen.blit(fontSuperSmall.render(line, True, white), (30, z))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isFirstTime = False
                running = False
                return

        pressedList = pygame.key.get_pressed()

        if pressedList[pygame.K_ESCAPE]:
            if flag_escape:
                beep.play()
                screen.fill(black)
                MakeStartMenu()
                break
            flag_escape = False
        else:
            flag_escape = True


def MakeRecordsMenu():
    global running, isFirstTime
    pygame.draw.line(screen, white, (10, 10), (590, 10), 3)
    pygame.draw.line(screen, white, (10, 10), (10, 390), 3)
    pygame.draw.line(screen, white, (10, 390), (590, 390), 3)
    pygame.draw.line(screen, white, (590, 10), (590, 390), 3)
    screen.blit(fontBig.render('Рекорды', True, brown), (215, 75))
    file = open("records.txt")
    z = 120
    counter = 1
    pointStartX = 230
    lines = file.readlines()
    for line in lines:
        z += 22
        if counter == 10:
            screen.blit(fontSmall.render(str(counter), True, white), (194, z))
        else:
            screen.blit(fontSmall.render(str(counter), True, white), (200, z))
        counter += 1
        for i in range(16):
            screen.blit(fontSmall.render('.', True, white), (pointStartX, z))
            pointStartX += 10
        pointStartX = 225
        screen.blit(fontSmall.render(line, True, white), (390, z))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isFirstTime = False
                running = False
                return

        pressedList = pygame.key.get_pressed()

        if pressedList[pygame.K_ESCAPE]:
            if flag_escape:
                beep.play()
                screen.fill(black)
                MakeStartMenu()
                break
            flag_escape = False
        else:
            flag_escape = True


def MakeGameOverMenu():
    global running, records
    if (currentScore > records[9]):
        records[9] = currentScore
        records.sort()
        records.reverse()
        fileToWrite = open('records.txt', 'w')
        for record in records:
            fileToWrite.write(str(record) + '\n')
        fileToWrite.close()
    game_over.play()
    onPlayButton = True
    onMenuButton = False
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, white, (10, 10), (590, 10), 3)
    pygame.draw.line(screen, white, (10, 10), (10, 390), 3)
    pygame.draw.line(screen, white, (10, 390), (590, 390), 3)
    pygame.draw.line(screen, white, (590, 10), (590, 390), 3)
    screen.blit(fontBig.render('Конец игры', True, brown), (178, 75))
    screen.blit(fontMedium.render('Score: ' + str(currentScore), True, white), (238, 140))
    pygame.draw.line(screen, white, (140, 208), (190, 208), 3)  # играть
    pygame.draw.line(screen, white, (411, 208), (461, 208), 3)  # играть
    screen.blit(fontSmall.render('заново', True, brown), (256, 200))
    screen.blit(fontSmall.render('главное меню', True, brown), (214, 250))
    pygame.display.flip()
    eggs.empty()
    timer = time.clock() + 15
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        # <editor-fold desc="Обработка нажатия клавиш">
        pressedList = pygame.key.get_pressed()
        if pressedList[pygame.K_UP] and onMenuButton:
            beep.play()
            if flag_up:
                DrawLines(white, black, black)
                onPlayButton = True
                onMenuButton = False
                pygame.display.flip()
            flag_up = False
        else:
            flag_up = True
        if pressedList[pygame.K_DOWN] and onPlayButton:
            beep.play()
            if flag_down:
                DrawLines(black, white, black)
                onPlayButton = False
                onMenuButton = True
                pygame.display.flip()
            flag_down = False
        else:
            flag_down = True
        if (pressedList[pygame.K_SPACE] or pressedList[pygame.K_RETURN]):
            if flag_space_return:
                if onPlayButton:
                    running = True
                    pygame.mixer.music.play(-1, 0.0)
                    time.sleep(0.3)
                    return
                if onMenuButton:
                    pygame.mixer.music.load('songs/metal.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1, 0.0)
                    time.sleep(0.15)  # опять же единственный выход, который я вижу, чтобы не было коллизий с кнопками
                    MakeStartMenu()
                    break
            flag_space_return = False
        else:
            flag_space_return = True
        if pressedList[pygame.K_ESCAPE]:
            if flag_esc:
                running = False
                return
            flag_esc = False
        else:
            flag_esc = True
        # </editor-fold>


def Pause():
    global running
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
        screen.fill(black)
        screen.blit(fontSmall.render('пауза', True, brown), (262, 150))
        screen.blit(fontSmall.render('для продолжения нажмите клавишу ПРОБЕЛ', True, white), (26, 230))
        pygame.display.update()
    timer = time.clock()


def KeyHandler(pressedList):
    global wolfIsTopRight, wolfIsTopLeft, wolfIsBottomLeft, wolfIsBottomRight
    if (pressedList[K_DOWN] and wolfIsTopRight):
        wolfIsBottomRight = True
        wolfIsTopRight = False
    if (pressedList[K_DOWN] and wolfIsTopLeft):
        wolfIsTopLeft = False
        wolfIsBottomLeft = True
    if (pressedList[K_UP] and wolfIsBottomRight):
        wolfIsBottomRight = False
        wolfIsTopRight = True
    if (pressedList[K_UP] and wolfIsBottomLeft):
        wolfIsBottomLeft = False
        wolfIsTopLeft = True
    if pressedList[K_RIGHT]:
        if wolfIsTopLeft:
            wolfIsTopLeft = False
            wolfIsTopRight = True
        elif wolfIsBottomLeft:
            wolfIsBottomLeft = False
            wolfIsBottomRight = True
        elif (wolfIsTopRight or wolfIsTopLeft or wolfIsBottomRight or wolfIsBottomLeft) == False:
            wolfIsTopRight = True
    if pressedList[K_LEFT]:
        if wolfIsTopRight:
            wolfIsTopRight = False
            wolfIsTopLeft = True
        elif wolfIsBottomRight:
            wolfIsBottomRight = False
            wolfIsBottomLeft = True
        elif (wolfIsTopRight or wolfIsTopLeft or wolfIsBottomRight or wolfIsBottomLeft) == False:
            wolfIsTopLeft = True
    if pressedList[K_p]:
        return Pause()


# </editor-fold>

# <editor-fold desc="Классы">
class Egg(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.xc = 0.0
        self.yc = 0.0
        self.move_time = 0.005

    def BecomeCaught(self):
        global currentScore, fromUpper, toastyTime, toastyClockStart, rabbit
        egg_caught.play()
        currentScore += 1
        if (currentScore % 13 == 0 and currentScore > 0):
            toasty.play()
            toastyClockStart = 200
            rabbit.reset_pos()
            toastyTime = True
        s = "I'm in!"
        fromUpper = False
        instructions = pygame.font.SysFont("Times New Roman", 15)
        if self.rect.x < 210:
            self.xc += 140
        else:
            self.xc -= 160
        screen.blit(instructions.render(s, True, (0, 255, 0)), (self.xc, self.yc + 21))
        pygame.display.update()
        if currentScore % 3 == 0 and self.move_time > 0:
            self.move_time -= 0.001
        if self.move_time < 0.002:
            self.move_time = 0
        time.sleep(self.move_time)
        self.rect.x = random.choice(xCoord)
        self.rect.y = random.choice(yCoord)
        self.xc = self.rect.x
        self.yc = self.rect.y
        fromUpper = False

    def update(self):
        global currentLifes, currentScore, fromUpper
        shelfFinished = False
        if self.rect.x < 200 or self.rect.x > 380:
            if self.rect.x < 210:
                self.rect.x += 1
                xFin = self.xc + 125
            else:
                self.rect.x -= 1
                xFin = self.xc - 125
            yFin = self.yc + 21
            a = (yFin - self.yc) / (xFin - self.xc)
            b = self.yc - a * self.xc
            self.rect.y = a * self.rect.x + b

        else:
            shelfFinished = True
            if 220 > self.rect.x >= 190 and self.rect.y < 150:
                if wolfIsTopLeft:
                    self.BecomeCaught()
                else:
                    fromUpper = True

            elif 375 <= self.rect.x <= 400 and self.rect.y < 150:
                if wolfIsTopRight:
                    self.BecomeCaught()
                else:
                    fromUpper = True

            elif 220 > self.rect.x >= 190 and wolfIsBottomLeft and 215 > self.rect.y >= 190 and not fromUpper:
                self.BecomeCaught()

            elif 375 <= self.rect.x <= 400 and wolfIsBottomRight and 215 > self.rect.y >= 190 and not fromUpper:
                self.BecomeCaught()

        if shelfFinished:
            if self.rect.y < 300 and shelfFinished:
                self.rect.y += 10
            if (self.rect.y >= 300):
                egg_cracking.play()
                s = "Crack!"
                fromUpper = False
                instructions = pygame.font.SysFont("Times New Roman", 18)
                currentLifes -= 1
                screen.blit(instructions.render(s, True, eggColor), (self.rect.x, self.rect.y))
                pygame.display.update()
                self.rect.x = self.xc = random.choice(xCoord)
                self.rect.y = self.yc = random.choice(yCoord)
        time.sleep(self.move_time)


class Rabbit(pygame.sprite.Sprite):

    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('images/toasty.png').convert_alpha(), (180, 119))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if (self.rect.x < 0):
            self.rect.x += 3.5

    def reset_pos(self):
        self.rect.x = -170
        self.rect.y = 280


# </editor-fold>

fileToRead = open('records.txt')
lines = fileToRead.readlines()
records = []
for line in lines:
    if line.strip():
        records.append(int(line))

rabbit = Rabbit()
AddEggs(eggs)
MakeStartMenu()

# <editor-fold desc="Игровой цикл">
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    DrawBackgroundInGame()
    DrawWolfWhereNeeded()
    pressedList = pygame.key.get_pressed()
    eggs.update()
    eggs.draw(screen)
    if KeyHandler(pressedList):
        running = False
        break

    if toastyTime and toastyClockStart > 0:
        rabbit.draw()
        rabbit.update()
        toastyClockStart -= 3

    pygame.display.update()

    if time.clock() - timer > 15 and len(eggs) < 4:
        timer = time.clock()
        AddEggs(eggs)

    if currentLifes == 0:
        pygame.mixer.music.stop()
        MakeGameOverMenu()
        if running and len(eggs) == 0:
            AddEggs(eggs)
        currentScore = 0
        currentLifes = 3
pygame.quit()
