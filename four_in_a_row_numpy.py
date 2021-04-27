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
        # this matrix represents the gameboard
        self.matrix = np.zeros((row, column), dtype=int)

        # dimensions of the matrix for indexing (max values for index)
        self.row: int = row - 1
        self.column: int = column - 1
        pass


# MAIN
def main():
    """The so called main-fuction.\n"""
    pass


if __name__ == '__main__':
    main()
