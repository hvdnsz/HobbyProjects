#!/usr/bin/python

#########
# PLANS #
#########
# TODO: SELECT COLUMN SUPER MARIO 2 DESIGN PICK UP AND PUT ON THE TOP OF HEAD


###########
# IMPORTS #
###########
import pygame
from pygame import Color
from four_in_a_row import Connect4GameBoard, player_switcher


#############
# CONSTANTS #
#############
# colors
BLACK = Color('black')
RED = Color('red')
BLUE = Color('blue')
YELLOW = Color('yellow')

# dimensions of the board
ROW = 6
COLUMN = 7

# dimensions of the tiles
TILE_SIZE = 100
TILE_PAD = 12

# dimensions of the screen
SCREEN_WIDTH = COLUMN * TILE_SIZE
SCREEN_HEIGHT = ROW * TILE_SIZE


#######################
# ASSEMBLE GAME TILES #
#######################
def draw_this(color, width, pad) -> pygame.Surface:
    image = pygame.Surface((width, width))

    radius = width // 2

    image.fill(BLUE)
    pygame.draw.circle(image, color, (radius, radius), radius - pad)

    return image


TILE_RED = draw_this(RED, TILE_SIZE, TILE_PAD)
TILE_YELLOW = draw_this(YELLOW, TILE_SIZE, TILE_PAD)
TILE_EMPTY = draw_this(BLACK, TILE_SIZE, TILE_PAD)


#####################################################
# VISUAL GAMEBOARD DISPLAYING THE ACTUAL GAME STATE #
#####################################################
class IAmTheVisualGameBoard(Connect4GameBoard):

    cuclik = {
        0: TILE_EMPTY,
        1: TILE_RED,
        2: TILE_YELLOW
    }

    def __init__(self, width: int, height: int):
        super(IAmTheVisualGameBoard, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill((250, 250, 250))

        self.part_width = width
        self.part_height = height

    def place_disk(self, col: int, player):
        row: int = self.search_row(col)
        if row != -1:
            self.matrix[row][col] = player

        # check win
        win = self.check_for_winning(row, col, player)
        if win:
            print(f'Player {player} has won!')

    def draw(self):
        pos_y = self.part_height

        # draw every tile depend on its id number
        for row in self.matrix:
            pos_y -= TILE_SIZE
            pos_x = 0
            for col in row:
                self.image.blit(self.cuclik[col], (pos_x, pos_y))
                pos_x += TILE_SIZE


#############################
# HANDLE THE DISPLAY SCREEN #
#############################
class MainWindow:

    def __init__(self):
        # init pygame
        pygame.init()

        # this is very temp or not
        self.done = False

        self.actual_p = player_switcher(1, 2)

        # init the screen
        pygame.display.set_caption('Four in a row :)')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # "static" part of the game
        self.gameboard = IAmTheVisualGameBoard(SCREEN_WIDTH, SCREEN_HEIGHT)

    def main_loop(self):
        done = False
        # main loop
        while not done:
            # main event loop
            # only for exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos_x = pygame.mouse.get_pos()[0]
                    player = next(self.actual_p)
                    self.gameboard.place_disk(mouse_pos_x // TILE_SIZE, player)
                    self.done = False

            # draw
            self.screen.fill((0, 0, 0))

            if not self.done:
                self.gameboard.draw()
                self.done = True

            self.screen.blit(self.gameboard.image, (0, 0))

            pygame.display.update()

        pygame.quit()


########
# MAIN #
########
game = MainWindow()
game.main_loop()