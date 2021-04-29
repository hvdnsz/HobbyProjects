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


class Connect4:
    def __init__(self, row=6, column=7):
        self.height: int = row
        self.width: int = column

        self.empty_field: str = '.'
        self.player_one: str = 'O'
        self.player_two: str = 'I'

        # ezek lesznek az oszlopok
        self.matrix: list[list] = [[self.empty_field for _ in range(column)] for _ in range(row)]

    def play_game(self):
        for player in cycle(self.player_one + self.player_two):
            self.print_matrix()
            print("it is the turn of player_" + player)

            while True:
                oszlop: int = int(input("Válaszd ki az oszlopot non zerobased: "))

                # test if the column is valid
                if self.validate_column(oszlop):
                    break

                print("nincs ilyen oszlop...próbáld meg újra")

            # to zero-vased indexing
            sor = self.keres_sor(oszlop)
            oszlop -= 1

            self.matrix[sor][oszlop] = player

            x_min, x_max, y_min, y_max = self.calculate_recangle(sor, oszlop)

            hor = self.horizontal(x_min, x_max, oszlop, sor, player)
            ver = self.vertical(oszlop, y_min, sor, player)
            d_left = self.diago_left(oszlop, sor, x_min, x_max, y_min, y_max, player)
            d_right = self.diago_right(oszlop, sor, x_min, x_max, y_min, y_max, player)

            if True in {hor, ver, d_left, d_right}:
                print('Játék vége!', player, ' nyert!')
                self.print_matrix()
                return

    def validate_column(self, col):
        """Validate the column in non-zerobased system.\n"""
        return True if 1 <= col <= self.width else False

    def keres_sor(self, col):
        for i in range(len(self.matrix)):
            if self.matrix[i][col] == self.empty_field:
                return i

    def print_matrix(self):
        print('#'*13)
        for sor in self.matrix[::-1]:
            print(' '.join(map(str, sor)))
        print('#'*13)

    def calculate_recangle(self, row: int, column: int) -> tuple[int, int, int, int]:  # this is zero-based
        """Azt számolja ki, hogy mennyi lehet hozzáadni az alap koordinátákhoz"""
        border_x: int = self.width - 1
        border_y: int = self.height - 1

        # horizont
        y_min: int = row if row < 3 else 3
        y_max: int = border_y - row if row > border_y - 3 else 3

        # ha nem lehet belőle kivonni hármat akkor önmaga különben 3
        x_min: int = column if column < 3 else 3
        x_max: int = border_x - column if column > border_x - 3 else 3

        return x_min, x_max, y_min, y_max

    def horizontal(self, x_min: int, x_max: int, x_constant: int,  y_constant: int, color: str) -> bool:
        """Ellenőrzi, hogy van-e négy egyforma színű az aktuális sorban.\n"""
        egyezes = 0

        for x in range(x_constant - x_min, x_constant + x_max+1):
            if self.matrix[y_constant][x] == color:
                egyezes += 1

                if egyezes == 4:
                    return True

            elif egyezes > 0:
                egyezes = 0

        return False

    def vertical(self, x_constant: int, y_min: int, y_constant: int, color: str) -> bool:
        """Ellenőrzi hogy van-e négy egyforma színű az aktuális oszlopban.\n"""
        egyezes = 0

        for y in range(y_constant - y_min, y_constant + 1):
            if self.matrix[y][x_constant] != color:
                return False
            else:
                egyezes += 1

            if egyezes >= 4:
                return True

        return False

    def diago_left(self, x_poz: int, y_poz: int, x_min: int, x_max: int, y_min: int, y_max: int, color: str) -> bool:
        """Ellenőrzi, hogy van-e egymás után négy egyforma színű, a balról-jobbra felfelé irányú átlóban.\n"""
        egyseges_balalso: int = self.take_smaller(x_min, y_min)
        egyseges_jobbfelso: int = self.take_smaller(x_max, y_max)

        egyezes = 0

        for x, y in zip(range(x_poz - egyseges_balalso, x_poz + egyseges_jobbfelso + 1, 1),
                        range(y_poz - egyseges_balalso, y_poz + egyseges_jobbfelso + 1, 1)):

            if self.matrix[y][x] == color:
                egyezes += 1

                if egyezes == 4:
                    return True

            elif egyezes > 0:
                egyezes = 0

        return False

    def diago_right(self, x_poz: int, y_poz: int, x_min: int, x_max: int, y_min: int, y_max: int, color: str) -> bool:
        """Ellenőrzi, hogy van-e egymás után négy egyforma színű, a balról-jobbra lefelé irányú átlóban.\n"""
        egyseges_balfelso: int = self.take_smaller(x_min, y_max)
        egyseges_jobbalso: int = self.take_smaller(x_max, y_min)

        egyezes = 0

        for x, y in zip(range(x_poz - egyseges_balfelso, x_poz + egyseges_jobbalso + 1, 1),
                        range(y_poz + egyseges_balfelso, y_poz - egyseges_jobbalso - 1, -1)):

            if self.matrix[y][x] == color:
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
    jatek = Connect4()
    jatek.play_game()
