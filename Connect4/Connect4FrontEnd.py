#!/usr/bin/python

#########
# PLANS #
#########
# TODO: SELECT COLUMN SUPER MARIO 2 DESIGN PICK UP AND PUT ON THE TOP OF HEAD


###########
# IMPORTS #
###########
import sys
import pygame
from pygame import Rect, Surface, Color
from pygame.font import Font
from Connect4BackEnd import Connect4GameBoard, player_switcher


#############
# CONSTANTS #
#############
# colors
BLACK = Color('black')
RED = Color(150, 0, 0)
BLUE = Color(0, 0, 150)
YELLOW = Color(150, 150, 0)
GREEN = Color(0, 150, 0)

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
def draw_this(color, width, pad) -> Surface:
    image = pygame.Surface((width, width))
    radius = width // 2
    image.fill(BLUE)
    pygame.draw.circle(image, color, (radius, radius), radius - pad)
    return image


TILE_RED: Surface = draw_this(RED, TILE_SIZE, TILE_PAD)
TILE_YELLOW: Surface = draw_this(YELLOW, TILE_SIZE, TILE_PAD)
TILE_EMPTY: Surface = draw_this(BLACK, TILE_SIZE, TILE_PAD)


#####################################################
# VISUAL GAME BOARD DISPLAYING THE ACTUAL GAME STATE #
#####################################################
class GameBoardUI(Connect4GameBoard):

    TILEMAP: dict[int, Surface] = {
        0: TILE_EMPTY,
        1: TILE_RED,
        2: TILE_YELLOW
    }

    def __init__(self, surface_rect: Rect, dimensions: tuple[int, int], tile_size: int) -> None:

        # init the inherited part of the class
        super(GameBoardUI, self).__init__(*dimensions)

        self.image: Surface = pygame.Surface((surface_rect.width, surface_rect.height))
        self.rect: Rect = surface_rect

        self.tile_size: int = tile_size

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def draw_all_tiles(self) -> None:
        """Draw all tiles to local image surface."""
        y: int = self.rect.bottom - self.tile_size
        for row in self.matrix:
            x: int = 0
            for tile_id in row:
                self.image.blit(self.TILEMAP[tile_id], (x, y))
                x += self.tile_size
            y -= self.tile_size


class GameOver:
    def __init__(self, pos: tuple[int, int], color: Color, size: int):
        # default color
        self.default_color: Color = color

        # just for safety
        pygame.font.init()
        # init font
        self.my_font: Font = pygame.font.Font(None, size)

        self.image: Surface = self.my_font.render('Default Text', True, self.default_color)
        # location of the text
        self.rect: Rect = self.image.get_rect(topleft=pos)

    def set_text(self, text: str, color=None):
        # optional parameter
        if color is None:
            color = self.default_color
        # re-render text to image surface
        self.image = self.my_font.render(text, True, color)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


#############################
# HANDLE THE DISPLAY SCREEN #
#############################
class MainWindow:

    def __init__(self):
        # init pygame
        pygame.init()

        # for switching between two players
        self.actual_p = player_switcher(1, 2)

        # init game over text
        # hardcoded
        self.game_over_screen = GameOver((TILE_SIZE + TILE_SIZE // 5, TILE_SIZE), GREEN, 80)

        # init display screen
        pygame.display.set_caption('Four in a row :)')
        flags: int = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

        # "static" part of the game
        self.game_board = GameBoardUI(Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), (6, 7), TILE_SIZE)

    def game_over(self, winner_player):
        self.game_over_screen.set_text(f"Player {winner_player} has won!")

    def main_loop(self):
        done: bool = False
        game_over: bool = False
        do_render: bool = True
        while not done:
            # clear event queue
            for event in pygame.event.get():
                # exit by pressing the red button
                if event.type == pygame.QUIT:
                    done = True
                # exit by pressing escape key
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    if event.key == pygame.K_r:
                        self.game_board.reset()
                        do_render = True
                        game_over = False

                elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # get the x value of the cursor
                    mouse_pos_x = event.pos[0]
                    # determine which column the cursor is in
                    column = mouse_pos_x // TILE_SIZE

                    # find the first free slot/row
                    free_row = self.game_board.search_row(column)

                    # there is a free row (the move is valid)
                    if free_row != -1:
                        # turn on render for this frame
                        do_render = True

                        # switch player
                        player = next(self.actual_p)

                        # place the disk
                        self.game_board.matrix[free_row][column] = player

                        # check if it was a winning move
                        win = self.game_board.check_for_winning(free_row, column, player)

                        # if it was "execute" game over process
                        if win:
                            self.game_over(player)
                            game_over = True

            # clear the screen with rgb black
            self.screen.fill((0, 0, 0))

            # redraw the game board
            self.game_board.draw_all_tiles()

            # blit to display
            self.game_board.draw(self.screen)

            # blit game over text
            if game_over:
                self.game_over_screen.draw(self.screen)

            # update the whole screen
            if do_render:
                do_render = False
                pygame.display.update()

        pygame.quit()


########
# MAIN #
########
def main() -> None:
    game = MainWindow()
    game.main_loop()
    sys.exit()


if __name__ == '__main__':
    main()
