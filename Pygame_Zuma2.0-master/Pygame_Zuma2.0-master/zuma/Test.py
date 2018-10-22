import pygame

pygame.init()

pygame.display.set_caption("Test")

height = 800
width = 800
size = [width, height]
screen = pygame.display.set_mode(size)
run = True
chick = pygame.image.load('pictures/chick.png')
duck = pygame.image.load('pictures/duck.png')
parrot = pygame.image.load('pictures/parrot.png')

#Всё, что потом надо вставить в код игры
pygame.font.init()

def well_done_draw(score):

    fontAcmeL = pygame.font.Font('Acme-Regular.ttf', 80)
    fontAcmeM = pygame.font.Font('Acme-Regular.ttf', 50)
    playerScoreSt = 'You have %s points!' % score
    playerScoreStEmpty = 'You have %s point!' % score

    textSurfaceWell = fontAcmeL.render('Well done!',True, (25, 25, 112))
    textSurfacePoint = fontAcmeM.render(playerScoreSt,True, (25, 25, 112))
    textSurfacePointEmpty = fontAcmeM.render(playerScoreStEmpty, True, (25, 25, 112))

    #эти две строчки не надо
    wellSize = pygame.font.Font.size(fontAcmeL, 'Well done!') #336, 102
    pointSize = pygame.font.Font.size(fontAcmeM, 'You have %s points!' % (score)) #439, 64


    screen.fill((255, 255, 255))
    screen.blit(textSurfaceWell, (232, 200))
    screen.blit(chick, (202, 650))
    screen.blit(parrot, (370, 650))
    screen.blit(duck, (558, 650))
    if (score == 0) or (score == -1) or (score == 1):
        screen.blit(textSurfacePointEmpty, (229, 400))
    else:
        screen.blit(textSurfacePoint, (190, 400))

def drow(score):
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False


        well_done_draw(score)
        pygame.display.flip()