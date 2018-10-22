import pygame

pygame.init()
title_font = pygame.font.SysFont('Comic Sans MS', 50)
subtitle_font = pygame.font.SysFont('Comic Sans MS', 40)
text_font = pygame.font.SysFont('Comic Sans MS', 35)
exit_font = pygame.font.SysFont('Comic Sans MS', 60)


class MenuViewElement(object):

    def __init__(self, size, label, font, colour, pos):
        self.pos = pos
        self.size = size
        self.label = label
        self.font = font
        self.colour = colour
        self.surface = pygame.Surface(self.size)

    def draw(self):
        text = self.font.render(self.label, 1, self.colour)
        text_height = text.get_height()
        ycoord = (self.surface.get_height() - text_height) / 2
        xcoord = (self.surface.get_width() - text.get_width()) / 2
        return text, (self.pos[0] + xcoord, self.pos[1] + ycoord)


class Info:

    def __init__(self, rect, colour, bg, text):
        self.pos = rect.topleft
        self.size = rect.size
        self.surf = pygame.Surface((rect.width, rect.height))
        self.colour = colour
        self.bg = bg
        self.text = text

    def update(self, state):

        y_pos = 0
        self.surf.blit(self.bg, (0, 0))
        for line in self.text[state]:
            if line is not None:
                text = line[2].render(line[0], 1, self.colour)
                if line[1] >= 0:
                    x_pos = line[1]
                    y_pos += text.get_height() + line[3]
                elif line[1] == -1:
                    x_pos = (self.size[0] - text.get_width()) / 2
                    y_pos = line[3]
                else:
                    x_pos = (self.size[0] - text.get_width()) / 2
                    y_pos = 175 + (50 - text.get_height()) / 2
                self.surf.blit(text, (x_pos, y_pos))
        return self


class Selector:

    def __init__(self, surf, bg, info, arrow):
        self.info = info
        self.bg = pygame.image.load(bg)
        self.state = 0
        self.surf = surf
        self.arrow = arrow

    def update(self):
        self.surf.blit(self.bg, (0, 0))
        if self.state == 0:
            self.surf.blit(self.arrow, (0, 0))
        elif self.state == 1:
            self.surf.blit(self.arrow, (0, 75))
        elif self.state == 2:
            self.surf.blit(self.arrow, (0, 150))
        self.info.update(self.state)

    def _down(self):
        if self.state != 2:
            self.state += 1
        else:
            self.state = 0

    def _up(self):
        if self.state != 0:
            self.state -= 1
        else:
            self.state = 2

    def _return(self):
        return self.state + 2


def load_scores(scores_file_name, score, name):
    if score >= 0:
        file = open(scores_file_name, 'a')
        if name == -1 or name == '':
            name = 'anon'
        if file.tell() != 0:
            file.write('\n' + name + '$' + str(score))
        else:
            file.write(name + '$' + str(score))
        file.close()
    file = open(scores_file_name, 'r')
    scores_list = []
    for line in file:
        lines = line.split('$')
        scores_list.append((lines[0], int(lines[1])), )
    scores_list.sort(key=lambda line: line[1], reverse=True)
    file = open(scores_file_name, 'w')

    prefix = ''
    i = 0
    for line in scores_list:
        if i >= 4:
            break
        file.write(prefix + line[0] + '$' + str(line[1]))
        prefix = '\n'
        i += 1
    file.close()
    scores_list = scores_list[:4]
    return scores_list


def menu(sel_rect, selector, screen, info, info_rect):
    running = True
    need_to_update = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 4
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selector._down()
                    need_to_update = True
                elif event.key == pygame.K_UP:
                    selector._up()
                    need_to_update = True
                elif event.key == pygame.K_RETURN:
                    sel_out = selector._return()
                    if sel_out != 3:
                        return sel_out
                    need_to_update = True

        if need_to_update:
            selector.update()
            screen.blit(selector.surf, sel_rect)
            screen.blit(info.surf, info_rect)
            pygame.display.update(sel_rect)
            pygame.display.update(info_rect)
            need_to_update = False


class Main:


    @staticmethod
    def load(game_name, score, name):
        scores = load_scores('scores.txt', score, name)
        scores_list_info = (("Play game", -1, title_font, 0),
                            ("Scores", -1, subtitle_font, 50))
        first_score_offset = 90
        for sc in scores:
            scores_list_info = scores_list_info + ((sc[0] + ' ' + str(sc[1]), -1, text_font, first_score_offset),)
            first_score_offset += 35

        info_text = (
            scores_list_info,
            (("Rules", -1, title_font, 0),
             ("You shoud stay live as long", 20, text_font, 20),
             ("as you can", 5, text_font, 5),
             ("Use UP, DOWN, LEFT and ", 20, text_font, 20),
             ("RIGTH buttons to move your", 5, text_font, 5),
             ("shuttle to avoid asteroids", 5, text_font, 5),
             ("Good luck!", 20, text_font, 10)),
            (("Exit game?", -2, exit_font),
             ("", -1, text_font, 0))
        )
        pygame.display.set_caption(game_name)
        screen = pygame.display.set_mode((600, 400), 0, 32)
        bg = pygame.image.load("data/menu/bg.png")
        WHITE = (255, 255, 255)

        title = MenuViewElement((550, 75), game_name, title_font, WHITE, (25, 25)) \
            .draw()
        play_button = MenuViewElement((125, 50), "Play", title_font, WHITE, (75, 150)).draw()
        rules_button = MenuViewElement((150, 50), "Rules", title_font, WHITE, (75, 225)).draw()
        exit_button = MenuViewElement((125, 50), "Exit", title_font, WHITE, (75, 300)).draw()
        info_rect = pygame.Rect((225, 125, 350, 250))
        info = Info(info_rect, WHITE, pygame.image.load('data/menu/info_bg.png'), info_text)
        sel_rect = pygame.Rect((25, 150, 50, 200))
        sel_arrow = pygame.image.load('data/menu/index.png')
        selector = Selector(pygame.Surface((50, 200)), "data//menu/sel_bg.png", info, sel_arrow)

        screen.blit(bg, (0, 0))
        screen.blit(title[0], title[1])
        screen.blit(play_button[0], play_button[1])
        screen.blit(rules_button[0], rules_button[1])
        screen.blit(exit_button[0], exit_button[1])

        pygame.display.flip()
        return menu(sel_rect, selector, screen, info, info_rect)
