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


plan = """
2D felülnézet minden egyes szabad hely tartalmazza hogy mennyi hiányzik még
keressen hármasokat, mert ha a vége azonos, akkor nyert
"""


class GameBoardConnect4:
    def __init__(self, empty: str, p1: str, p2: str, row=6, column=7) -> None:
        # dimensions
        self.height: int = row
        self.width: int = column

        # log last move
        self.last_x: int = 0
        self.last_y: int = 0
        # sub_y/y, add_x/y
        self.sub_x: int = 0
        self.sub_y: int = 0
        self.add_x: int = 0
        self.add_y: int = 0

        # fields representes as strings
        self.empty_field: str = empty
        self.player_one: str = p1
        self.player_two: str = p2

        # ezek lesznek az oszlopok
        self.matrix: list[list] = [[self.empty_field for _ in range(column)] for _ in range(row)]

    def calculate_rectangle(self, row: int, column: int) -> tuple[int, int, int, int]:  # this is zero-based
        """Azt számolja ki, hogy mennyi lehet hozzáadni az alap koordinátákhoz"""
        border_x: int = self.width - 1
        border_y: int = self.height - 1

        # vertical
        sub_x = column if column < 3 else 3
        add_x = border_x - column if column > border_x - 3 else 3

        # horizontal
        sub_y = row if row < 3 else 3
        add_y = border_y - row if row > border_y - 3 else 3

        return sub_x, add_x, sub_y, add_y

    def horizontal(self, player: str) -> bool:
        """Ellenőrzi, hogy van-e négy egyforma színű az aktuális sorban.\n"""
        egyezes = 0

        for x in range(self.last_x - self.sub_x, self.last_x + self.add_x + 1):
            if self.matrix[self.last_y][x] == player:
                egyezes += 1

                if egyezes == 4:
                    return True

            elif egyezes > 0:
                egyezes = 0

        return False

    def vertical(self, player: str) -> bool:
        """Ellenőrzi hogy van-e négy egyforma színű az aktuális oszlopban.\n"""
        egyezes = 0

        for y in range(self.last_y - self.sub_y, self.last_y + 1):
            if self.matrix[y][self.last_x] != player:
                return False
            else:
                egyezes += 1

            if egyezes >= 4:
                return True

        return False

    def diago_left(self, player: str) -> bool:
        """Ellenőrzi, hogy van-e egymás után négy egyforma színű, a balról-jobbra felfelé irányú átlóban.\n"""
        egyseges_balalso: int = self.take_smaller(self.sub_x, self.sub_y)
        egyseges_jobbfelso: int = self.take_smaller(self.add_x, self.add_y)

        egyezes = 0

        for x, y in zip(range(self.last_x - egyseges_balalso, self.last_x + egyseges_jobbfelso + 1, 1),
                        range(self.last_y - egyseges_balalso, self.last_y + egyseges_jobbfelso + 1, 1)):

            if self.matrix[y][x] == player:
                egyezes += 1

                if egyezes == 4:
                    return True

            elif egyezes > 0:
                egyezes = 0

        return False

    def diago_right(self, player: str) -> bool:
        """Ellenőrzi, hogy van-e egymás után négy egyforma színű, a balról-jobbra lefelé irányú átlóban.\n"""
        egyseges_balfelso: int = self.take_smaller(self.sub_x, self.add_y)
        egyseges_jobbalso: int = self.take_smaller(self.add_x, self.sub_y)

        egyezes = 0

        for x, y in zip(range(self.last_x - egyseges_balfelso, self.last_x + egyseges_jobbalso + 1, 1),
                        range(self.last_y + egyseges_balfelso, self.last_y - egyseges_jobbalso - 1, -1)):

            if self.matrix[y][x] == player:
                egyezes += 1

                if egyezes == 4:
                    return True

            elif egyezes > 0:
                egyezes = 0

        return True if egyezes >= 4 else False

    @staticmethod
    def take_smaller(a, b):
        return a if a < b else b


if __name__ == '__main__':
    pass
