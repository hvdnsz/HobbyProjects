#!/usr/bin/python
"""
The classic game of Connect Four is played by two players in a grid of 6 row_count
by 7 column_count, standing vertically. Players alternately drop one token from
the top of one column, and the token falls to the lowest possible grid cell,
stacking up on the tokens below it. The first player to make a horizontal,
vertical or diagonal line of 4 tokens wins the game.
From the description of one game grid, your program must determine in which
column_count each player may complete a line if they play first on the next turn.
"""
from enum import Enum


# UTILS
def player_switcher(p1, p2):
    while True:
        yield p1
        yield p2


def force_within_range(min_: int, max_: int, prompt: str) -> int:
    while True:
        out = int(input(prompt))
        if min_ <= out <= max_:
            return out

        print('This option is invalid...try again!')


class FieldMark(Enum):
    EMPTY = 0
    PLAYER_1 = 1
    PLAYER_2 = 2


class Connect4GameBoard:
    # CONSTANTS
    EMPTY_FIELD = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2

    def __init__(self, row=6, column=7) -> None:
        # dimensions
        self.row_count: int = row
        self.column_count: int = column

        self.disks_played: int = 0
        self.disks_limit: int = row * column

        # this is the structure of the game board
        self._init_matrix()

    def _init_matrix(self) -> None:
        self.matrix: list[list] = [[self.EMPTY_FIELD for _ in range(self.column_count)] for _ in range(self.row_count)]

    def reset(self) -> None:
        self._init_matrix()

    def place_disk(self, col: int, row: int, disk: int) -> None:
        self.matrix[row][col] = disk

    def search_row(self, col: int) -> int:
        """
        Find the index of the lowest free row (if there is one).
        :param col: index of the column
        :type col: int
        :return: the index of the first free row or None
        """

        # now the user can give float like this (2.0)
        col = int(col)

        for i, row in enumerate(self.matrix):
            if row[col] == self.EMPTY_FIELD:
                return i
        else:
            return -1

    def check_for_winning(self, row: int, col: int, player) -> bool:  # this is zero-based
        """Calculate the minimal free space around a disk/coordination and check winning."""
        border_x: int = self.column_count - 1
        border_y: int = self.row_count - 1

        # horizontal
        sub_x = min(3, col)
        add_x = min(3, border_x - col)
        # vertical
        sub_y = min(3, row)
        add_y = min(3, border_y - row)

        def check_direction(start_x: int, end_x: int, start_y: int, end_y: int, dx: int, dy: int) -> bool:
            """attention end_x: last index of x (range + 1) end_y: last index of y (range + 1)"""

            # pointers
            x: int = start_x
            y: int = start_y
            # count consecutive disks
            matches: int = 0

            while x <= end_x and y <= end_y:
                if self.matrix[y][x] == player:
                    matches += 1
                    if matches == 4:
                        return True
                elif matches > 0:
                    matches = 0

                # increment pointers
                x += dx
                y += dy

            return False

        # horizontal
        horizontal: bool = check_direction(col - sub_x, col + add_x, row, row, 1, 0)
        # vertical
        vertical: bool = check_direction(col, col, row - sub_y, row + add_y, 0, 1)
        # diagonals go from left to right
        # diagonal /
        lb: int = min(sub_x, sub_y)
        rt: int = min(add_x, add_y)
        diagonal_lb_rt: bool = check_direction(col - lb, col + rt, row - lb, col + rt, 1, 1)
        # diagonal \
        lt: int = min(sub_x, add_y)
        rb: int = min(add_x, sub_y)
        # end_y is border_y + 1 because y is decreasing. This won't cause any error since  x and y are synchronized.
        diagonal_lt_rb: bool = check_direction(col - lt, col + rb, row + lt, border_y + 1, 1, -1)

        return max(horizontal, vertical, diagonal_lb_rt, diagonal_lt_rb)


class Connect4Game(Connect4GameBoard):

    def __init__(self, player1=None, player2=None):
        super(Connect4Game, self).__init__()
        if player1 is not None:
            self.PLAYER_ONE = player1
        if player2 is not None:
            self.PLAYER_TWO = player2

    def print_matrix(self) -> None:
        """Just the print the matrix human readable."""
        print('#' * 13)
        for sor in self.matrix[::-1]:
            print(' '.join(map(str, sor)))
        print('#' * 13)

    def play_game(self):
        print('The game has begun!!!')

        result_of_the_game = None

        for actual_player in player_switcher(self.PLAYER_ONE, self.PLAYER_TWO):

            # the game board is full
            if self.disks_played > self.disks_limit:
                result_of_the_game = 'draw'
                break

            # inform the player about the actual state
            self.print_matrix()
            print('It is the turn of player -', actual_player)

            # get a valid column
            column: int = int(input('pleas enter the number: ')) - 1
            # get the row
            for i, row in enumerate(self.matrix):
                if row[column] == self.EMPTY_FIELD:
                    row = i
                    break
            else:
                row = 0

            # place/drop a disk from the actual player
            self.matrix[row][column] = actual_player

            # check winning
            if self.check_for_winning(row, column, actual_player):
                result_of_the_game = str(actual_player) + ' win!!!'
                break

        self.print_matrix()
        print('the result is:', result_of_the_game)


def main():
    game = Connect4Game()
    game.play_game()


if __name__ == '__main__':
    main()
    exit()
