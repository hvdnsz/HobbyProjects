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

    def __init__(self, width: int, height: int, pos):
        super(IAmTheVisualGameBoard, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill((250, 250, 250))

        self.pos = pos

        self.part_width = width
        self.part_height = height

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.pos)

    def redraw_tiles(self):
        pos_y = self.part_height

        # draw every tile depend on its id number
        for row in self.matrix:
            pos_y -= TILE_SIZE
            pos_x = 0
            for col in row:
                self.image.blit(self.cuclik[col], (pos_x, pos_y))
                pos_x += TILE_SIZE


class GameOver:
    def __init__(self, pos, color, size: int):

        # location of the text
        self.pos = pos
        self.default_color = color

        # just for safety
        pygame.font.init()
        self.my_font = pygame.font.Font(None, size)
        self.text = self.my_font.render('Default Text', True, (100, 100, 100))

    def set_text(self, text: str, color=None):
        # optional parameter
        if color is None:
            color = self.default_color

        self.text = self.my_font.render(text, True, color)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.text, self.pos)


#############################
# HANDLE THE DISPLAY SCREEN #
#############################
class MainWindow:

    def __init__(self):
        # init pygame
        pygame.init()

        # for switching between two players
        self.actual_p = player_switcher(1, 2)

        # game over text init
        # hardcoded
        self.game_over_screen = GameOver((TILE_SIZE + 20, TILE_SIZE), PURPLE, 80)

        # init the screen
        pygame.display.set_caption('Four in a row :)')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # "static" part of the game
        self.gameboard = IAmTheVisualGameBoard(SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0))

        # render list for organizing the objects waiting for render
        self.render_list: list = []
        self.render_list.append(self.gameboard)

    def render(self):
        for sprite in self.render_list:
            sprite.draw(self.screen)

    def game_over(self, winner_player):

        self.game_over_screen.set_text(f"Player {winner_player} has won!")
        self.render_list.append(self.game_over_screen)

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

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                            self.game_over(player)

            # clear the screen with rgb black
            self.screen.fill((0, 0, 0))

            # redraw the gameboard
            self.gameboard.redraw_tiles()

            # draw all active sprites
            self.render()

            # update the whole screen
            pygame.display.update()

        pygame.quit()


########
# MAIN #
########
game = MainWindow()
game.main_loop()
