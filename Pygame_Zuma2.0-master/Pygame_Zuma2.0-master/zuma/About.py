import pygame
import Menu
pygame.init()

pygame.display.set_caption("About")

height = 800
width = 800
size = [width, height]
screen = pygame.display.set_mode(size)
run = True
chick = pygame.image.load('pictures/chick.png')
duck = pygame.image.load('pictures/duck.png')
parrot = pygame.image.load('pictures/parrot.png')
bg = pygame.image.load('pictures/fon.jpg')
goBack = pygame.image.load('pictures/goBack.png')
flag = False

pygame.font.init()


def drow_about():

    fontAcmeL = pygame.font.Font('Acme-Regular.ttf', 80)
    fontAcmeM = pygame.font.Font('Acme-Regular.ttf', 50)
    fontAcmeS = pygame.font.Font('Acme-Regular.ttf', 30)


    textSurfaceHello = fontAcmeL.render('Hello!',True, (25, 25, 112))
    textSurfaceWe = fontAcmeM.render('We are Niaz and Dilyara' ,True, (25, 25, 112))
    textSurfaceHope = fontAcmeM.render('We hope you enjoy our game' ,True, (25, 25, 112))
    textSurfaceGoBack = fontAcmeS.render('back', True, (25, 25, 112))

    helloSize = pygame.font.Font.size(fontAcmeL, 'Hello!') #188, 102
    weSize = pygame.font.Font.size(fontAcmeM, 'We are Niaz and Dilyara') #473, 64
    hopeSize = pygame.font.Font.size(fontAcmeM, 'We hope you enjoy our game') # 593, 64



    screen.blit(bg, (0,0))
    screen.blit(goBack, (0,0))
    screen.blit(textSurfaceGoBack, (20, 65))
    screen.blit(textSurfaceHello, (306, 150))
    screen.blit(textSurfaceWe, (163, 300))
    screen.blit(textSurfaceHope, (120, 400))
    screen.blit(chick, (202, 650))
    screen.blit(parrot, (370, 650))
    screen.blit(duck, (538, 650))


def drow():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                global flag
                flag = True
                run = False

        drow_about()

        pygame.display.flip()