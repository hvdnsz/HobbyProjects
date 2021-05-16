#!/usr/bin/python
"""
The classic game of Connect Four is played by two players in a grid of 6 rows
by 7 columns, standing vertically. Players alternately drop one token from
the top of one column, and the token falls to the lowest possible grid cell,
stacking up on the tokens below it. The first player to make a horizontal,
vertical or diagonal line of 4 tokens wins the game.

From the description of one game grid, your program must determine in which
columns each player may complete a line if they play first on the next turn.
"""
from enum import Enum


class Cases(Enum):
    COLUMN_IS_VALID = 0
    COLUMN_IS_FILLED = 1
    COLUMN_IS_INAPPROPRIATE = 2

    # I'm not sure
    PLAYER_1_WIN = 3
    PLAYER_2_WIN = 4
    DRAW = 5


class Connect4Engine(object):
    # CONSTANTS
    EMPTY_FIELD = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2

    def __init__(self, row=6, column=7) -> None:
        # dimensions
        self.height: int = row
        self.width: int = column

        # this is the structure of the game board
        self.matrix: list[list] = [[self.EMPTY_FIELD for _ in range(column)] for _ in range(row)]

    def give_back_a_magic_number(self, column):
        pass

    def check_for_winning(self, row: int, column: int, player) -> bool:  # this is zero-based
        """Calculate the minimal free space around a disk/coordination."""
        # todo: potential performance issue
        border_x: int = self.width - 1
        border_y: int = self.height - 1

        # horizontal todo mennyi a különbség comma potential helper function
        sub_x = column if column < 3 else 3
        add_x = border_x - column if column > border_x - 3 else 3
        # vertical
        sub_y = row if row < 3 else 3
        add_y = border_y - row if row > border_y - 3 else 3

        def check_horizontal_line() -> bool:
            matches = 0
            for x in range(row - sub_x, row + add_x + 1):
                if self.matrix[column][x] == player:
                    matches += 1
                elif matches > 0:
                    matches = 0

                if matches == 4:
                    return True
            return False

        def check_vertical_line() -> bool:
            matches = 0
            for y in range(column - sub_y, column + add_y):
                if self.matrix[y][row] != player:
                    return False
                matches += 1

            # do not check the current disk
            return True if matches == 3 else False

        def check_diagonal_line(left_corner, right_corner) -> bool:
            matches = 0
            for x, y in zip(range(row - left_corner, row + right_corner + 1),
                            range(column - left_corner, column + right_corner + 1)):
                if self.matrix[y][x] == player:
                    matches += 1
                elif matches > 0:
                    matches = 0

                if matches == 4:
                    return True

            return False

        # TODO polishing: give me some optimisation
        horizontal = check_horizontal_line()
        vertical = check_vertical_line()
        left_bottom_right_top = check_diagonal_line(min(sub_x, sub_y), min(add_x, add_y))
        right_bottom_left_top = check_diagonal_line(min(sub_x, add_y), min(add_x, sub_y))

        if any([horizontal, vertical, left_bottom_right_top, right_bottom_left_top]):
            return True
        else:
            return False

    def print_matrix(self):
        print('#' * 13)
        for sor in self.matrix[::-1]:
            print(' '.join(map(str, sor)))
        print('#' * 13)
