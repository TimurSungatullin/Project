import MainMenu
import pygame

title_font = pygame.font.SysFont('Comic Sans MS', 50)
subtitle_font = pygame.font.SysFont('Comic Sans MS', 40)
text_font = pygame.font.SysFont('Comic Sans MS', 35)
exit_font = pygame.font.SysFont('Comic Sans MS', 60)


def check_input(name, events):
    state = 0
    for event in events:
        if event.type == pygame.KEYDOWN:
            if pygame.K_a <= event.key <= pygame.K_z:
                name += chr(event.key)
            if event.key == pygame.K_BACKSPACE:
                name = name[:-1]
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            state = 4
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            state = 1
    return name, state

def menu(screen, bg):
    running = True
    name = ""
    input_rect = pygame.Rect((25, 275, screen.get_width() - 50, 50))
    font = pygame.font.SysFont('Comic Sans MS', 40)
    while running:
        name, state = check_input(name, pygame.event.get())
        if state == 4:
            return 4, -1
        elif state == 1:
            return 1, name
        text = font.render("Write your name: " + name, 1, (255, 255, 255))
        screen.blit(bg, (0, 0))
        x_pos = (input_rect.width - text.get_width()) / 2
        y_pos = input_rect.topleft[1] + (input_rect.height - text.get_height()) / 2
        screen.blit(text, (x_pos, y_pos))
        pygame.display.update(input_rect)

class Main:

    pygame.init()

    @staticmethod
    def load(game_name, score):
        score_text = 'Your score ' + score
        text = (
            None,
            (("GAME OVER", -1, title_font, 150),
             (score_text, -1, subtitle_font, 200),
             ("Press enter button to continue", -1, text_font, 350)),
        )
        pygame.display.set_caption(game_name)
        screen = pygame.display.set_mode((600, 400), 0, 32)
        bg = pygame.image.load("data/menu/bg.png")
        WHITE = (255, 255, 255)

        info_rect = pygame.Rect((0, 0, 600, 400))
        info = MainMenu.Info(info_rect, WHITE, bg, text)
        info.update(1)
        screen.blit(bg, (0, 0))
        screen.blit(info.surf, info_rect)

        pygame.display.flip()
        menu(screen, bg)
