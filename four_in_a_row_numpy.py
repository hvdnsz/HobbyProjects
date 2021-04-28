#!/usr/bin/python
"""
Python version 3.9 and above. (not use typing library)
Four in a row terminal/console implementation based on numpy.
Windows: pip install numpy
Linux: pip3 install numpy
"""

# IMPORTS
import numpy as np


# this class handle the gameboard
class GameBoard:
    """A numpy-based gameboard\n"""

    def __init__(self, row: int, column: int):
        """Init the matrix storing the state of the game.\n"""
        # define the numbers representing the players and blank fields
        self.blank_field: int = 0
        self.player_1: int = 1
        self.player_2: int = 2

        # this matrix represents the gameboard
        self.matrix = np.zeros((row, column), dtype=int)

        # dimensions of the matrix for indexing (max values for index)
        self.row: int = row - 1
        self.column: int = column - 1
        pass

    def search_free_row(self, col: int):
        """Find the next free row in the matrix (to insert a disk).\n"""
        for i, row in enumerate(self.matrix):
            if row[col] != 0:
                return i
        return None

    def validate_column(self, col: int) -> bool:
        """Validate the collumn to insert the 'korong'.\n"""
        return True if 0 <= col <= self.column else False

    def insert_disk(self, row: int, col: int, color: int) -> None:
        """Insert a colored disc into the matrix colomn-th column.\n"""
        self.matrix[row, col] = color
        pass

    def print_matrix(self):
        """Print the matrix on terminal/console in numpy style.\n"""
        print(self.matrix[::-1])

    def clear_matrix(self):
        """Set every values of the matrix to zero.\n"""
        self.matrix = np.zeros((self.row+1, self.column+1))


# MAIN
def main():
    """The so called main-fuction.\n"""
    pass


if __name__ == '__main__':
    main()
