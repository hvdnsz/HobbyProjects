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
from itertools import cycle


def force_within_range(min_: int, max_: int, prompt: str) -> int:
    while True:
        out = int(input(prompt))
        if min_ <= out <= max_:
            return out

        print('This option is invalid...try again!')


class Connect4Engine:
    def __init__(self, empty='.', p1='O', p2='I', row=6, column=7) -> None:
        # dimensions
        self.height: int = row
        self.width: int = column

        # fields represents as strings
        self.empty_field: str = empty
        self.player_one: str = p1
        self.player_two: str = p2

        # this is the structure of the game board
        self.matrix: list[list] = [[self.empty_field for _ in range(column)] for _ in range(row)]

    def _authorize_move(self, column):
        """This is zero-based."""
        passed = True

        # in case of too big or small column
        if column < 0 or column >= self.width:
            passed = False

        # in case of full bar
        self._check_bar(column)

    def _apply_move(self):
        pass

    def _calculate_free_space(self, row: int, column: int) -> dict:  # this is zero-based
        """Calculate the minimal free space around a disk/coordination."""
        # todo: potential performance issue
        border_x: int = self.width - 1
        border_y: int = self.height - 1

        # vertical
        sub_x = column if column < 3 else 3
        add_x = border_x - column if column > border_x - 3 else 3

        # horizontal
        sub_y = row if row < 3 else 3
        add_y = border_y - row if row > border_y - 3 else 3

        out = {
            0: sub_x,
            1: add_x,
            2: sub_y,
            3: add_y
        }

        return out

    def _check_wining(self, x, y):
        pass

    def _check_bar(self, column):
        for i, row in enumerate(self.matrix):
            if row[column] != self.empty_field:
                return i
        return None

    # COMPLEMENT BUILT-IN PLAY FUNCTION
    def print_matrix(self):
        print('#' * 13)
        for sor in self.matrix[::-1]:
            print(' '.join(map(str, sor)))
        print('#' * 13)
