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


class Connect4GameBoard(object):
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
        self.matrix: list[list] = [[self.EMPTY_FIELD for _ in range(column)] for _ in range(row)]

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

    def check_for_winning(self, row: int, column: int, player) -> bool:  # this is zero-based
        """Calculate the minimal free space around a disk/coordination and check winning."""
        # todo: potential performance issue
        border_x: int = self.column_count - 1
        border_y: int = self.row_count - 1

        # horizontal todo mennyi a különbség comma potential helper function
        sub_x = column if column < 3 else 3
        add_x = border_x - column if column > border_x - 3 else 3
        # vertical
        sub_y = row if row < 3 else 3
        add_y = border_y - row if row > border_y - 3 else 3

        def check_horizontal_line() -> bool:
            matches = 0
            for x in range(column - sub_x, column + add_x + 1):

                if self.matrix[row][x] == player:
                    matches += 1
                    if matches == 4:
                        return True

                elif matches > 0:
                    matches = 0

            return False

        def check_vertical_line() -> bool:
            matches = 0
            for y in range(row - sub_y, row):
                if self.matrix[y][column] != player:
                    return False
                matches += 1

            # do not check the current disk
            return True if matches == 3 else False

        def check_lb_rt_diagonal_line() -> bool:
            matches = 0
            left_corner = min(sub_x, sub_y)
            right_corner = min(add_x, add_y)

            for x, y in zip(range(column - left_corner, column + right_corner + 1),
                            range(row - left_corner, row + right_corner + 1)):
                if self.matrix[y][x] == player:
                    matches += 1
                    if matches == 4:
                        return True

                elif matches > 0:
                    matches = 0

            return False

        def check_lt_rb_diagonal_line() -> bool:
            matches = 0
            left_corner = min(sub_x, add_y)
            right_corner = min(add_x, sub_y)

            for x, y in zip(range(column - left_corner, column + right_corner + 1),
                            range(row + left_corner, row - right_corner - 1, -1)):  # y is decreasing
                if self.matrix[y][x] == player:
                    matches += 1
                    if matches == 4:
                        return True

                elif matches > 0:
                    matches = 0

            return False

        for func in (check_horizontal_line, check_vertical_line, check_lt_rb_diagonal_line, check_lb_rt_diagonal_line):
            if func() is True:
                return True

        return False


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
