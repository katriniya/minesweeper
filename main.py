import pygame
import random

pygame.font.init()

# CHANGE VALUE
END_COL = 9

COLOR_BG = (255, 204, 255)  # pink
COLOR_BOMB = (178, 34, 34)  # red
COLOR_0 = (154, 205, 50)  # green
COLOR_FLAG = (50, 105, 250)  # green
SQUARE_LIST = []
NO_BOMB = 0
DEMINING = 0
GAME_OVER = False
APP_RUNNING = True
VALUE_GAME_OVER = ''
FONT = pygame.font.SysFont('Comic Sans MS', END_COL*5)
COUNT_BOMB = int(END_COL*1.5)

def create_square():
    for i in range(2, (END_COL+1)*50, 50):
        objlist_min = []
        for k in range(2, (END_COL+1)*50, 50):
            objlist_min.append(Square(i, k))
        SQUARE_LIST.append(objlist_min)

    for l in range(0, COUNT_BOMB, 1):
        bomb_x = random.randint(0, END_COL)
        bomb_y = random.randint(0, END_COL)

        while SQUARE_LIST[bomb_x][bomb_y].bomb:
            bomb_x = random.randint(0, END_COL)
            bomb_y = random.randint(0, END_COL)

        SQUARE_LIST[bomb_x][bomb_y].bomb = True

        SQUARE_LIST[bomb_x][bomb_y].color_vl = pygame.Color(*COLOR_BOMB)

    for z in range(len(SQUARE_LIST)):
        for k in range(len(SQUARE_LIST)):
            if SQUARE_LIST[z][k].bomb:
                count_bomb_around(z, k)


def count_bomb_around(x, y):  # paint over cells near bombs

    for j in range(-1, 2, 1):
        for k in range(-1, 2, 1):
            if (0 <= (x + j) <= END_COL) and \
                    (0 <= (y + k) <= END_COL) and \
                    (not SQUARE_LIST[x + j][y + k].bomb):
                SQUARE_LIST[x + j][y + k].count_bomb += 1


def open_cell(x, y): #open zero-zone
    if SQUARE_LIST[x][y].count_bomb == 0:
        for j in range(-1, 2, 1):
            for k in range(-1, 2, 1):
                if (0 <= (x + j) <= END_COL) and (0 <= (y + k) <= END_COL)\
                        and SQUARE_LIST[x + j][y + k].color_bg != SQUARE_LIST[x + j][y + k].color_vl:

                    SQUARE_LIST[x + j][y + k].color_bg = SQUARE_LIST[x + j][y + k].color_vl

                    font = pygame.font.SysFont('Comic Sans MS', 30)
                    SQUARE_LIST[x + j][y + k].text = font.render(str(SQUARE_LIST[x + j][y + k].count_bomb), True, pygame.Color(255, 255, 255))
                    SQUARE_LIST[x + j][y + k].draw_square(game.screen)

                    global NO_BOMB
                    NO_BOMB += 1

                    if SQUARE_LIST[x + j][y + k].count_bomb == 0:
                        open_cell(x + j, y + k)


class Game:

    def __init__(self):
        self.width = (END_COL+1)*50
        self.height = (END_COL+1)*50
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.go_surf = FONT.render('Game over', True, pygame.Color(2, 5, 0), pygame.Color(200, 250, 200))
        self.gw_surf = FONT.render('YOU WIN', True, pygame.Color(2, 5, 0), pygame.Color(200, 250, 200))
        self.restart = FONT.render('Press R to restart', True, pygame.Color(2, 5, 0), pygame.Color(200, 250, 200))

        pygame.display.set_caption('MINESWEEPER')
        create_square()

    def draw_game_over(self, value):
        center_game_go = self.go_surf.get_rect(center=(self.width/2, self.height/2.5))
        center_game_gw = self.gw_surf.get_rect(center=(self.width/2, self.height/2.5))
        center_restart = self.restart.get_rect(center=(self.width/2, self.height/1.8))

        if value == 'win':
            self.screen.blit(self.gw_surf, center_game_gw)
        else:
            self.screen.blit(self.go_surf, center_game_go)

        self.screen.blit(self.restart, center_restart)

    def draw_game(self, value):

        self.screen.fill((43, 43, 43))

        for i in SQUARE_LIST:
            for a in i:
                a.draw_square(self.screen)

        if GAME_OVER:
            game.draw_game_over(value)

        pygame.display.flip()


class Square:
    def __init__(self, x, y):
        self.width = 45
        self.height = 45
        self.obj_x = x
        self.obj_y = y
        self.bomb = False
        self.flag = False
        self.count_bomb = 0
        self.color_bg = pygame.Color(*COLOR_BG)
        self.color_vl = pygame.Color(*COLOR_0)
        self.text = FONT.render('', True, pygame.Color(255, 255, 255))

    def draw_square(self, screen):
        pygame.draw.rect(screen, self.color_bg, pygame.Rect(self.obj_x, self.obj_y, self.width, self.height))

        center_number = self.text.get_rect(center=(self.obj_x+self.width/2, self.obj_y+20))
        screen.blit(self.text, center_number)

    def update_object(self, value):
        if value == 'click':
            self.color_bg = self.color_vl
            global NO_BOMB
            if not self.bomb:
                font = pygame.font.SysFont('Comic Sans MS', 30)
                self.text = font.render(str(self.count_bomb), True, pygame.Color(255, 255, 255))
                NO_BOMB += 1

                if self.count_bomb == 0:
                    open_cell(int((self.obj_x - 2) / 50), int((self.obj_y - 2) / 50))
        else:
            self.flag_check()
            global DEMINING
            DEMINING += 1 if self.flag else -1


    def flag_check(self):
        if i.flag:
            i.flag = False
            i.color_bg = pygame.Color(*COLOR_BG)
        else:
            i.flag = True
            i.color_bg = pygame.Color(*COLOR_FLAG)


if __name__ == '__main__':

    game = Game()

    while APP_RUNNING:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                APP_RUNNING = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    GAME_OVER = False
                    SQUARE_LIST = []
                    NO_BOMB = 0
                    DEMINING = 0
                    VALUE_GAME_OVER = ''
                    create_square()

        pressed = pygame.mouse.get_pressed()

        if pressed[0] and not GAME_OVER:
            mouse_press = pygame.mouse.get_pos()

            for y in SQUARE_LIST:
                for i in y:
                    if i.obj_x <= mouse_press[0] <= i.obj_x + 45 \
                            and i.obj_y <= mouse_press[1] <= i.obj_y + 45 \
                            and i.color_bg != i.color_vl:
                        i.update_object('click')
                        if i.bomb:
                            GAME_OVER = True
                            VALUE_GAME_OVER = 'game_over'


        if pressed[2] and not GAME_OVER:  # check bomb
            mouse_press = pygame.mouse.get_pos()

            for y in SQUARE_LIST:
                for i in y:

                    if i.obj_x <= mouse_press[0] <= i.obj_x + 45 and\
                            i.obj_y <= mouse_press[1] <= i.obj_y + 45 \
                            and i.color_bg != i.color_vl:

                        i.update_object('flag')

                        print(DEMINING)

        if NO_BOMB == ((END_COL+1)**2 - COUNT_BOMB) or DEMINING == COUNT_BOMB:
            GAME_OVER = True
            VALUE_GAME_OVER = 'win'

        game.draw_game(VALUE_GAME_OVER)
