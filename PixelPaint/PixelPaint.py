#!usr/bin/python
import pygame
from pygame import Rect, Surface
from random import randint
import sys


# type alias for color pixel
RGBColor = tuple[int, int, int]
Pos = tuple[int, int]


# helper/util functions for RGBColor
def random_color() -> RGBColor:
    """Generate a pseudo-random RGB color"""
    r: int = randint(0, 255)
    g: int = randint(0, 255)
    b: int = randint(0, 255)
    return r, g, b


def rgb2gray_average(color: RGBColor) -> int:
    """Basic grayscale conversion based on the average of RGB color channels."""
    return sum(color) // 3


# class for the pixel grid
class Canvas:
    def __init__(self, dimensions: Pos, pixel_width: int) -> None:
        # row and column count
        self.cols: int = dimensions[0]
        self.rows: int = dimensions[1]

        # size of a pixel in the grid
        self.pixel_width: int = pixel_width

        # absolute position
        self.image: Surface = Surface((self.cols * self.pixel_width, self.rows * self.pixel_width))
        self.rect: Rect = self.image.get_rect()

        # 2D grid list [x][y] indexing
        self._init_grid(color=(0, 56, 0))

        # draw initialised grid
        self.draw_all_pixels()

    def fill_grid(self, color: RGBColor) -> None:
        """Wrapper for privat _init_grid helper method."""
        self._init_grid(color)
        self.draw_all_pixels()

    def _init_grid(self, color: RGBColor = (0, 0, 0)) -> None:
        self._grid: list[list[RGBColor]] = [[color for _ in range(self.rows)] for _ in range(self.cols)]

    @property
    def grid(self) -> list[list[RGBColor]]:
        return self._grid

    def flood_fill(self, mouse_pos: Pos, target_color: RGBColor) -> None:
        # relative positions
        x: int = mouse_pos[0] // self.pixel_width
        y: int = mouse_pos[1] // self.pixel_width

        # this color should be changed
        # there is a bug when try to target_color == base_color
        base_color: RGBColor = self._grid[x][y]
        if base_color == target_color:
            return

        # uncolored tiles only valid ones
        stack: list[Pos] = [(x, y)]

        while stack:
            # we can assume that first x and y is valid
            # so we only have to check x+1, x-1. y+1, y-1
            x, y = stack.pop()

            # on go on if we are still in base zone
            if self._grid[x][y] == base_color:
                self._grid[x][y] = target_color

                # draw change immediately
                pygame.draw.rect(
                    self.image,
                    target_color,
                    (x * self.pixel_width, y * self.pixel_width, self.pixel_width, self.pixel_width)
                )

                # push neighbours to stack
                if x > 0:
                    stack.append((x - 1, y))
                if x < self.cols - 1:
                    stack.append((x + 1, y))
                if y > 0:
                    stack.append((x, y - 1))
                if y < self.rows - 1:
                    stack.append((x, y + 1))

        return

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def draw_all_pixels(self) -> None:
        rect_to_draw: Rect = Rect(0, 0, self.pixel_width, self.pixel_width)
        for col in range(self.cols):
            rect_to_draw.y = 0
            for row in range(self.rows):
                pygame.draw.rect(self.image, self._grid[col][row], rect_to_draw)
                rect_to_draw.y += self.pixel_width
            rect_to_draw.x += self.pixel_width

    def color_pixel(self, mouse_pos: Pos, color: RGBColor) -> None:
        # relative positions
        col: int = mouse_pos[0] // self.pixel_width
        row: int = mouse_pos[1] // self.pixel_width
        self._grid[col][row] = color
        pygame.draw.rect(
            self.image,
            color,
            (col * self.pixel_width, row * self.pixel_width, self.pixel_width, self.pixel_width)
        )


# main window is the only one
class MainWindow:
    def __init__(self):
        pygame.init()

        # canvas owns the full screen
        self.canvas: Canvas = Canvas((64, 36), 20)

        # display flags
        flags: int = 0

        # canvas owns the full screen
        self.screen: Surface = pygame.display.set_mode(self.canvas.rect.bottomright, flags)

    def run(self):
        done: bool = False
        color: RGBColor = (255, 0, 0)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    elif event.key == pygame.K_f:
                        self.canvas.fill_grid(color)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.canvas.color_pixel(event.pos, color)
                    elif event.button == 4:
                        # change active color to something random
                        color = random_color()
                    elif event.button == 5:
                        col: int = event.pos[0] // self.canvas.pixel_width
                        row: int = event.pos[1] // self.canvas.pixel_width
                        # color pick
                        # using property
                        color = self.canvas.grid[col][row]
                    elif event.button == 3:
                        self.canvas.flood_fill(event.pos, color)
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:
                        self.canvas.color_pixel(event.pos, color)

            # # draw canvas onto MainWindow's display
            self.canvas.draw(self.screen)

            # update MainWindow's display
            pygame.display.flip()


def main() -> None:
    window = MainWindow()
    window.run()

    # brutal exit
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
