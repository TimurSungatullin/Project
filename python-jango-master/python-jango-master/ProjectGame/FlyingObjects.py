import pygame, os


class FlyingObjects(pygame.sprite.Sprite):
    def __init__(self, img, cX, cY):
        # Создаем спрайт из картинки
        pygame.init()
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = self.load_image(img, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Перемещаем картинку в её начальные координаты
        self.rect.x = cX
        self.rect.y = cY

    def load_image(self, name, colorkey=None):  # отображение картинок
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        #image = image.convert()
        #if colorkey is not None:
        #    if colorkey is -1:
        #        colorkey = image.get_at((0, 0))
        #    image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image, image.get_rect()
