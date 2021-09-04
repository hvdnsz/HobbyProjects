#!usr/bin/python
import pygame.examples.mask
from pygame import Vector2, Surface, Color
import sys
from random import randint


# dimension
CELL_UNIT: int = 50
GRID_SIZE: int = 20
# geometry
ROUNDING: int = 10
# refresh rate
FPS: int = 5


# util function
def draw_rect_from_pos(pos: Vector2, screen: Surface, color: Color) -> None:
    pygame.draw.rect(
        screen,
        color,
        (pos * CELL_UNIT, (CELL_UNIT, CELL_UNIT)),
        border_radius=ROUNDING
    )


def generate_random_pos() -> Vector2:
    return Vector2(randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1))


def facing_from_vector(v: Vector2) -> int:
    if v.y == -1:
        return 0
    elif v.x == 1:
        return 2
    elif v.y == 1:
        return 4
    elif v.x == -1:
        return 6
    else:
        raise Exception(f'Invalid head direction:{v}')


head: Surface = pygame.image.load('Snake_head_up.png')
vertical: Surface = pygame.image.load('Snake_body_vertical.png')
turning: Surface = pygame.image.load('Snake_turning_topright.png')
tail: Surface = pygame.image.load('Snake_tail_up.png')
# flip tail since its direction is to opposite of its facing
tail = pygame.transform.flip(tail, False, True)


head_graphics: dict[int, Surface] = {facing: pygame.transform.rotate(head, -90 * (facing / 2))
                                     for facing in range(0, 7, 2)}
tail_graphics: dict[int, Surface] = {facing: pygame.transform.rotate(tail, -90 * (facing / 2))
                                     for facing in range(0, 7, 2)}
middle_graphics: dict[int, Surface] = {
    0: pygame.transform.rotate(vertical, 0),    # vertical
    1: pygame.transform.rotate(vertical, -90),  # horizontal
    2: pygame.transform.rotate(turning, 0),
    3: pygame.transform.rotate(turning, -90),
    4: pygame.transform.rotate(turning, -180),
    5: pygame.transform.rotate(turning, -270)
}


class Snake:
    directions: dict[int, Vector2] = {
        pygame.K_UP: Vector2(0, -1),
        pygame.K_DOWN: Vector2(0, 1),
        pygame.K_LEFT: Vector2(-1, 0),
        pygame.K_RIGHT: Vector2(1, 0)
    }

    def __init__(self):
        # hardcoded initial position and direction
        self._direction: Vector2 = self.directions[pygame.K_RIGHT]
        self._body: list[Vector2] = [Vector2(2, 0), Vector2(1, 0), Vector2(0, 0)]

        # states
        self._is_growing: bool = False
        self._is_alive: bool = True

    def reset(self) -> None:
        self.__init__()

    def change_direction(self, key: int) -> None:
        new_direction: Vector2 = self.directions.get(key)
        if new_direction is None or not self._direction + new_direction:
            return
        self._direction = new_direction

    def update(self) -> None:
        # get the new head
        new_head: Vector2 = self.head + self._direction

        # check collision itself and the walls
        if new_head in self._body[:-1] or not 0 <= new_head.x < GRID_SIZE or not 0 <= new_head.y < GRID_SIZE:
            self._is_alive = False
            return

        # grow the snake
        self._body.insert(0, new_head)

        if self._is_growing:
            self._is_growing = False
            return

        # shrink the snake
        self._body.pop()

    def let_it_grow(self) -> None:
        self._is_growing = True

    def collide_point(self, pos: Vector2) -> bool:
        return pos in self._body

    # noinspection PyTypeChecker
    # blit do not support Vector2 as destination yet
    def draw(self, screen: Surface) -> None:
        # draw head
        screen.blit(head_graphics[facing_from_vector(self._body[0] - self._body[1])], self._body[0] * CELL_UNIT)
        # draw tail
        screen.blit(tail_graphics[facing_from_vector(self._body[-2] - self._body[-1])], self._body[-1] * CELL_UNIT)
        # draw other parts
        image: Surface
        for i, pos in enumerate(self._body[1:-1], start=1):
            dir_to_pos: Vector2 = pos - self._body[i + 1]       # closer to tail
            dir_to_next_pos: Vector2 = self._body[i - 1] - pos  # closer to head
            # check easier cases
            if dir_to_pos.x * dir_to_next_pos.x:
                image = middle_graphics[1]
            elif dir_to_pos.y * dir_to_next_pos.y:
                image = middle_graphics[0]
            # save some check with seemingly unnecessary else
            else:
                # check turnings
                if (dir_to_pos.y == -1 and dir_to_next_pos.x == 1) or (dir_to_pos.x == -1 and dir_to_next_pos.y == 1):
                    image = middle_graphics[2]
                elif (dir_to_pos.x == 1 and dir_to_next_pos.y == 1) or (dir_to_pos.y == -1 and dir_to_next_pos.x == -1):
                    image = middle_graphics[3]
                elif (dir_to_pos.y == 1 and dir_to_next_pos.x == -1) or (dir_to_pos.x == 1 and dir_to_next_pos.y == -1):
                    image = middle_graphics[4]
                # lets hope there will be no error in the game logic (there should be)
                else:
                    image = middle_graphics[5]

            # draw the correct part onto the screen
            screen.blit(image, pos * CELL_UNIT)

    @property
    def head(self) -> Vector2:
        return self._body[0]

    @property
    def is_alive(self) -> bool:
        return self._is_alive


class GameLogic:
    def __init__(self):
        # init pygame
        pygame.init()

        # init display window
        self.screen: Surface = pygame.display.set_mode((CELL_UNIT * GRID_SIZE, CELL_UNIT * GRID_SIZE))
        pygame.display.set_caption('Snake')

        # init snake
        self.snake: Snake = Snake()

        # fruit will be only a Vector by the simplicity of the game
        self.fruit: Vector2 = generate_random_pos()

        # to trigger gameover
        self.is_gameover: bool = False

    def on_update(self) -> None:
        # update snake (without shrink it's size)
        self.snake.update()

        # check if the snake is alive
        if not self.snake.is_alive:
            self.is_gameover = True
            return

        # check fruit collision
        if self.snake.head == self.fruit:
            while self.snake.collide_point(self.fruit):
                self.fruit = generate_random_pos()
            self.snake.let_it_grow()

    def on_draw(self) -> None:
        # clear the screen
        self.screen.fill(Color('black'))

        # draw the snake (fruit will have been repositioned)
        self.snake.draw(self.screen)

        # draw the fruit
        draw_rect_from_pos(self.fruit, self.screen, Color('green'))

        # refresh full screen
        pygame.display.flip()

    def run(self) -> None:
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    # update snake's position
                    self.snake.change_direction(event.key)

            # freeze screen if the game is over
            if not self.is_gameover:
                # update the game
                self.on_update()
            else:
                self.snake.reset()
                self.is_gameover = False

            # render the game
            self.on_draw()


def main() -> None:
    GameLogic().run()


if __name__ == '__main__':
    main()
