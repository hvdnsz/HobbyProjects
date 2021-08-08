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
PURPLE = Color('purple')

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

        # init basic font system
        self.my_font = pygame.font.Font(None, 128)

        # for switching between two players
        self.actual_p = player_switcher(1, 2)

        # duck tape for game over
        self.is_game_over = False

        # init the screen
        pygame.display.set_caption('Four in a row :)')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # "static" part of the game
        self.gameboard = IAmTheVisualGameBoard(SCREEN_WIDTH, SCREEN_HEIGHT)

    def game_over(self, winner_player):
        pass

    def main_loop(self):
        done = False
        # main loop
        while not done:

            # event loop to clear the event queue
            for event in pygame.event.get():
                # exit by pressing the red button
                if event.type == pygame.QUIT:
                    done = True
                # exit by pressing escape key
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True

                # handle the left mouse button
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
                        not self.is_game_over:
                    # get the x value of the cursor
                    mouse_pos_x = pygame.mouse.get_pos()[0]
                    # determine which column the cursor is in
                    column = mouse_pos_x // TILE_SIZE

                    # keres egy szabad sort
                    szabad_sor = self.gameboard.search_row(column)

                    # there is a free row (the move is valid)
                    if szabad_sor != -1:

                        # switch player
                        player = next(self.actual_p)

                        # place the disk
                        self.gameboard.matrix[szabad_sor][column] = player

                        # check if it was a winning move
                        win = self.gameboard.check_for_winning(szabad_sor, column, player)

                        # if it was "execute" game over process
                        if win:
                            self.is_game_over = True

            # clear the screen with rgb black
            self.screen.fill((0, 0, 0))

            # redraw the gameboard
            self.gameboard.draw()
            self.screen.blit(self.gameboard.image, (0, 0))

            # drawing the game over text
            # over the game board
            if self.is_game_over:
                # TODO: I am really sorry, please fix me soon :(
                # line 134 and __init__

                next(self.actual_p)
                game_over_text = self.my_font.render('Game Over!', True, PURPLE)
                self.screen.blit(game_over_text, (TILE_SIZE, TILE_SIZE))

            # update the whole screen
            pygame.display.update()

        pygame.quit()


########
# MAIN #
########
game = MainWindow()
game.main_loop()
